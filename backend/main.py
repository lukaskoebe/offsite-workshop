"""FastAPI backend for the Recipe Book app.

Serves recipe data from the SQLite database at ../data/recipes.db.
Run with:  uv run uvicorn main:app --reload --port 8001
"""

import json
import os
import sqlite3
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

# Override with RECIPES_DB_PATH (used by tests to point at a temp database).
DB_PATH = Path(
    os.environ.get(
        "RECIPES_DB_PATH",
        Path(__file__).resolve().parent.parent / "data" / "recipes.db",
    )
)

# Serve the interactive API docs under /api so they're reachable through the
# Vite dev proxy (http://localhost:3000/api/docs).
app = FastAPI(
    title="Recipe Book API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
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
