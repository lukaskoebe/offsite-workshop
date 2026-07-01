"""Create and seed the recipe database.

Run standalone to reset the database to its sample state:

    uv run python seed.py

`init_db` and `seed_recipes` are also imported by the test suite.
The database location follows the same RECIPES_DB_PATH override as main.py.
"""

import json
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(
    os.environ.get(
        "RECIPES_DB_PATH",
        Path(__file__).resolve().parent.parent / "data" / "recipes.db",
    )
)

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    image TEXT NOT NULL,
    prep_time INTEGER NOT NULL,
    cook_time INTEGER NOT NULL,
    servings INTEGER NOT NULL,
    difficulty TEXT NOT NULL CHECK(difficulty IN ('easy', 'medium', 'hard')),
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL
)
"""

SEED_RECIPES = [
    {
        "title": "Spaghetti Carbonara",
        "description": "A classic Roman pasta dish made with eggs, pecorino cheese, guanciale, and black pepper.",
        "image": "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=800&q=80",
        "prep_time": 10,
        "cook_time": 20,
        "servings": 4,
        "difficulty": "medium",
        "ingredients": [
            "400g spaghetti",
            "200g guanciale or pancetta",
            "4 large eggs",
            "100g pecorino romano, grated",
            "100g parmesan, grated",
            "Freshly ground black pepper",
            "Salt",
        ],
        "instructions": [
            "Bring a large pot of salted water to a boil. Cook spaghetti according to package directions until al dente.",
            "While pasta cooks, cut guanciale into small strips and cook in a cold skillet over medium heat until crispy and fat renders.",
            "In a bowl, whisk eggs with grated pecorino and parmesan.",
            "Remove skillet from heat. Drain pasta, reserving 1 cup of pasta water.",
            "Add hot pasta to the skillet with guanciale. Toss quickly, then pour egg mixture over pasta, tossing vigorously.",
            "Add pasta water a little at a time until sauce is creamy and coats the pasta.",
            "Serve immediately with lots of black pepper and extra cheese.",
        ],
    },
    {
        "title": "Chicken Tikka Masala",
        "description": "Tender chunks of marinated chicken in a rich, creamy tomato-based curry sauce.",
        "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800&q=80",
        "prep_time": 30,
        "cook_time": 40,
        "servings": 6,
        "difficulty": "medium",
        "ingredients": [
            "800g boneless chicken thighs",
            "200ml plain yogurt",
            "2 tbsp tikka masala paste",
            "2 onions, finely diced",
            "4 garlic cloves, minced",
            "1 tbsp ginger, grated",
            "400g canned crushed tomatoes",
            "200ml heavy cream",
            "2 tbsp butter",
            "1 tsp turmeric",
            "1 tsp cumin",
            "Salt and cilantro to taste",
        ],
        "instructions": [
            "Cut chicken into chunks. Mix yogurt with tikka paste and marinate chicken for at least 30 minutes.",
            "Grill or broil chicken until charred. Set aside.",
            "In a large pan, melt butter and sauté onions until golden. Add garlic and ginger, cook 1 minute.",
            "Add turmeric, cumin, and crushed tomatoes. Simmer 15 minutes until thickened.",
            "Stir in heavy cream. Add chicken and simmer 10 more minutes.",
            "Season with salt. Garnish with fresh cilantro. Serve with basmati rice or naan.",
        ],
    },
    {
        "title": "Classic Margherita Pizza",
        "description": "Authentic Neapolitan pizza with San Marzano tomatoes, fresh mozzarella, basil, and olive oil.",
        "image": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800&q=80",
        "prep_time": 120,
        "cook_time": 15,
        "servings": 2,
        "difficulty": "hard",
        "ingredients": [
            "500g bread flour",
            "325ml warm water",
            "10g salt",
            "3g active dry yeast",
            "200g San Marzano tomatoes, crushed",
            "250g fresh mozzarella, sliced",
            "Fresh basil leaves",
            "Extra virgin olive oil",
        ],
        "instructions": [
            "Dissolve yeast in warm water. Mix flour and salt, then add yeast water. Knead 10 minutes until smooth.",
            "Cover and let rise 2 hours until doubled.",
            "Divide dough into 2 balls. Let rest 30 minutes.",
            "Preheat oven to 250°C (500°F) with a pizza stone or baking sheet inside.",
            "Stretch each ball into a 12-inch round on a floured surface.",
            "Spread crushed tomatoes on base. Add mozzarella slices. Drizzle with olive oil.",
            "Bake 10-15 minutes until crust is golden and cheese bubbles.",
            "Top with fresh basil leaves and serve immediately.",
        ],
    },
    {
        "title": "Avocado Toast",
        "description": "Simple and satisfying smashed avocado on sourdough with chili flakes and lemon.",
        "image": "https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=800&q=80",
        "prep_time": 5,
        "cook_time": 5,
        "servings": 2,
        "difficulty": "easy",
        "ingredients": [
            "2 slices sourdough bread",
            "2 ripe avocados",
            "1 lemon, juiced",
            "Red chili flakes",
            "Flaky sea salt",
            "Extra virgin olive oil",
        ],
        "instructions": [
            "Toast sourdough slices until golden and crisp.",
            "Cut avocados in half, remove pits, and scoop flesh into a bowl.",
            "Mash with a fork to desired consistency. Add lemon juice and mix.",
            "Spread smashed avocado on each toast slice.",
            "Drizzle with olive oil, sprinkle chili flakes and sea salt. Serve immediately.",
        ],
    },
    {
        "title": "Thai Green Curry",
        "description": "Aromatic coconut-based curry with green curry paste, vegetables, and your choice of protein.",
        "image": "https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=800&q=80",
        "prep_time": 15,
        "cook_time": 25,
        "servings": 4,
        "difficulty": "medium",
        "ingredients": [
            "400ml coconut milk",
            "3 tbsp green curry paste",
            "400g chicken breast, sliced",
            "1 bell pepper, sliced",
            "1 zucchini, sliced",
            "100g green beans",
            "2 tbsp fish sauce",
            "1 tbsp brown sugar",
            "Thai basil leaves",
            "Jasmine rice for serving",
        ],
        "instructions": [
            "Cook jasmine rice according to package directions.",
            "In a wok or large pan, heat a splash of coconut cream from the top of the can. Fry curry paste 2 minutes until fragrant.",
            "Add chicken and cook until sealed on all sides.",
            "Pour in remaining coconut milk. Add fish sauce and brown sugar. Simmer 10 minutes.",
            "Add bell pepper, zucchini, and green beans. Cook 5 more minutes.",
            "Stir in Thai basil. Serve over jasmine rice.",
        ],
    },
    {
        "title": "Chocolate Lava Cake",
        "description": "Individual molten chocolate cakes with a gooey liquid center. A decadent dessert.",
        "image": "https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=800&q=80",
        "prep_time": 15,
        "cook_time": 12,
        "servings": 4,
        "difficulty": "hard",
        "ingredients": [
            "200g dark chocolate (70%)",
            "120g unsalted butter",
            "3 large eggs",
            "3 egg yolks",
            "100g caster sugar",
            "40g all-purpose flour",
            "Butter and cocoa for ramekins",
            "Vanilla ice cream to serve",
        ],
        "instructions": [
            "Preheat oven to 200°C (400°F). Butter 4 ramekins and dust with cocoa powder.",
            "Melt chocolate and butter together in a heatproof bowl over simmering water. Stir until smooth. Let cool slightly.",
            "In a separate bowl, whisk eggs, egg yolks, and sugar until thick and pale, about 3 minutes.",
            "Fold chocolate mixture into egg mixture. Sift flour over and fold gently.",
            "Divide batter among ramekins. Place on a baking tray.",
            "Bake 12 minutes — edges should be firm but center should jiggle.",
            "Let rest 30 seconds. Run a knife around edges, invert onto plates.",
            "Serve immediately with vanilla ice cream.",
        ],
    },
]


def init_db(conn: sqlite3.Connection) -> None:
    """Create the recipes table if it does not exist."""
    conn.execute(CREATE_TABLE)


def seed_recipes(conn: sqlite3.Connection) -> None:
    """Replace all rows with the sample recipes (idempotent reset)."""
    conn.execute("DELETE FROM recipes")
    conn.execute("DELETE FROM sqlite_sequence WHERE name = 'recipes'")
    conn.executemany(
        """
        INSERT INTO recipes
            (title, description, image, prep_time, cook_time,
             servings, difficulty, ingredients, instructions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                r["title"],
                r["description"],
                r["image"],
                r["prep_time"],
                r["cook_time"],
                r["servings"],
                r["difficulty"],
                json.dumps(r["ingredients"]),
                json.dumps(r["instructions"]),
            )
            for r in SEED_RECIPES
        ],
    )


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)
        seed_recipes(conn)
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
    finally:
        conn.close()
    print(f"Seeded {count} recipes into {DB_PATH}")


if __name__ == "__main__":
    main()
