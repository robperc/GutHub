import sqlite3
from contextlib import closing

class Database:
    def __init__(self, db_path="recipes.db", connection=None):
        """Initialize the database connection."""
        self.connection = connection or sqlite3.connect(db_path, check_same_thread=False)
        self._initialize_database()

    def _initialize_database(self):
        """Create the recipes table if it doesn't exist."""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    ingredients TEXT,
                    instructions TEXT,
                    categories TEXT
                )
            """)
            self.connection.commit()

    def save_recipe(self, name, url, ingredients, instructions, categories):
        """Save a recipe to the database."""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                INSERT OR IGNORE INTO recipes (name, url, ingredients, instructions, categories)
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                url,
                "\n".join(ingredients),  # Save ingredients as a newline-separated string
                "\n".join(instructions),  # Save instructions as a newline-separated string
                ", ".join(categories)  # Save categories as a comma-separated string
            ))
            self.connection.commit()

    def fetch_recipe_by_name(self, name):
        """Fetch a recipe by its name."""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM recipes WHERE name = ?", (name,))
            return cursor.fetchone()

    def fetch_recipe_by_id(self, recipe_id):
        """Fetch a recipe by its ID."""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "url": row[2],
                    "ingredients": row[3].split("\n") if row[3] else [],
                    "instructions": row[4].split("\n") if row[4] else [],
                    "categories": row[5].split(", ") if row[5] else []
                }
            return None

    def fetch_all_recipes(self):
        """Fetch all recipes from the database."""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM recipes")
            return cursor.fetchall()

    def delete_recipe(self, recipe_id):
        """Delete a recipe by its ID."""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            self.connection.commit()

    def update_recipe(self, recipe_id, name=None, ingredients=None, instructions=None, categories=None):
        """Update a recipe's details by its ID."""
        with closing(self.connection.cursor()) as cursor:
            if name:
                cursor.execute("UPDATE recipes SET name = ? WHERE id = ?", (name, recipe_id))
            if ingredients:
                cursor.execute("UPDATE recipes SET ingredients = ? WHERE id = ?", ("\n".join(ingredients), recipe_id))
            if instructions:
                cursor.execute("UPDATE recipes SET instructions = ? WHERE id = ?", ("\n".join(instructions), recipe_id))
            if categories:
                cursor.execute("UPDATE recipes SET categories = ? WHERE id = ?", (", ".join(categories), recipe_id))
            self.connection.commit()