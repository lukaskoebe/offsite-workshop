"""FastAPI backend for the Recipe Book app.

Serves recipe data from the SQLite database at ../data/recipes.db.
Run with:  uv run uvicorn main:app --reload --port 8001
"""

import json
import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field, ValidationError

from ai import ask_ai, ask_ai_json
from seed import init_db, seed_recipes

# Override with RECIPES_DB_PATH (used by tests to point at a temp database).
DB_PATH = Path(
    os.environ.get(
        "RECIPES_DB_PATH",
        Path(__file__).resolve().parent.parent / "data" / "recipes.db",
    )
)


def ensure_db() -> None:
    """Make sure the database exists and has data.

    On a fresh checkout the `data/` directory and SQLite file don't exist yet
    (the DB is gitignored), so opening it would fail with "unable to open
    database file". Create the directory + table, and seed sample recipes if
    the table is empty.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)
        (count,) = conn.execute("SELECT COUNT(*) FROM recipes").fetchone()
        if count == 0:
            seed_recipes(conn)
        conn.commit()
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_db()
    yield


# Serve the interactive API docs under /api so they're reachable through the
# Vite dev proxy (http://localhost:3000/api/docs).
app = FastAPI(
    title="Recipe Book API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)


class RecipeInput(BaseModel):
    title: str = Field(min_length=1)
    description: str
    image: str = ""
    prepTime: int = Field(ge=0)
    cookTime: int = Field(ge=0)
    servings: int = Field(ge=1)
    difficulty: Literal["easy", "medium", "hard"]
    ingredients: list[str]
    instructions: list[str]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_summary(row: sqlite3.Row) -> dict:
    """Fields used by the recipe list view."""
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "image": row["image"],
        "prepTime": row["prep_time"],
        "cookTime": row["cook_time"],
        "servings": row["servings"],
        "difficulty": row["difficulty"],
    }


def row_to_recipe(row: sqlite3.Row) -> dict:
    """Full recipe, with JSON columns parsed into lists."""
    return {
        **row_to_summary(row),
        "ingredients": json.loads(row["ingredients"]),
        "instructions": json.loads(row["instructions"]),
    }


@app.get("/api/recipes")
def list_recipes() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM recipes ORDER BY id").fetchall()
    return [row_to_summary(row) for row in rows]


@app.get("/api/recipes/{recipe_id}")
def get_recipe(recipe_id: int) -> dict:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM recipes WHERE id = ?", (recipe_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return row_to_recipe(row)


@app.post("/api/recipes", status_code=201)
def create_recipe(recipe: RecipeInput) -> dict:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO recipes
                (title, description, image, prep_time, cook_time,
                 servings, difficulty, ingredients, instructions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                recipe.title,
                recipe.description,
                recipe.image,
                recipe.prepTime,
                recipe.cookTime,
                recipe.servings,
                recipe.difficulty,
                json.dumps(recipe.ingredients),
                json.dumps(recipe.instructions),
            ),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM recipes WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return row_to_recipe(row)


@app.delete("/api/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int) -> Response:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return Response(status_code=204)


# --------------------------------------------------------------------------
# AI features
#
# Example endpoint showing how to build an AI feature. It calls the ask-ai API
# through the `ask_ai` helper (see ai.py) — copy this pattern for other AI
# features (e.g. "make this recipe vegetarian", "scale to N servings").
# In tests, mock `ask_ai` instead of calling the live API.
# --------------------------------------------------------------------------


class RecipeIdeasInput(BaseModel):
    ingredients: list[str] = Field(min_length=1)


@app.post("/api/ai/recipe-ideas")
def recipe_ideas(body: RecipeIdeasInput) -> dict:
    """Free-text example: suggest recipes from a list of ingredients."""
    prompt = (
        "Suggest 3 recipes I could make with these ingredients: "
        + ", ".join(body.ingredients)
        + ". For each, give a title and one sentence."
    )
    suggestions = ask_ai(prompt, system="You are a concise, helpful chef.")
    return {"suggestions": suggestions}


class RecipeIdeaPrompt(BaseModel):
    idea: str = Field(min_length=1)


@app.post("/api/ai/generate-recipe")
def generate_recipe(body: RecipeIdeaPrompt) -> RecipeInput:
    """Structured-output example: turn a short idea into a full recipe.

    The pattern for reliable structured AI output:
      1. Ask for JSON (`ask_ai_json` requests JSON mode).
      2. Describe the exact shape you want in the prompt.
      3. Validate the parsed JSON against a Pydantic model (`RecipeInput`), so
         the route returns typed data the frontend can use directly — e.g. to
         prefill the add-recipe form. Bad output fails loudly (502) instead of
         reaching the client malformed.
    """
    prompt = (
        f"Create a recipe for: {body.idea}.\n"
        "Return a JSON object with exactly these keys: "
        'title (string), description (string), image (string, use ""), '
        "prepTime (integer minutes), cookTime (integer minutes), "
        "servings (integer), difficulty (one of \"easy\", \"medium\", \"hard\"), "
        "ingredients (array of strings), instructions (array of strings)."
    )
    data = ask_ai_json(prompt, system="You are a chef that replies with strict JSON only.")
    try:
        return RecipeInput.model_validate(data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI returned an unexpected recipe shape: {exc.errors()}",
        ) from exc
