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

    def fetch_all_recipes(self):
        """Fetch all recipes from the database."""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM recipes")
            return cursor.fetchall()

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

    def delete_recipe(self, recipe_id):
        """Delete a recipe from the database by its ID."""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            self.connection.commit()
            print(f"Recipe with ID {recipe_id} deleted.")

    def update_recipe(self, recipe_id, name=None, url=None, ingredients=None, instructions=None, categories=None):
        """Update a recipe in the database."""
        with closing(self.connection.cursor()) as cursor:
            updates = []
            params = []
            if name:
                updates.append("name = ?")
                params.append(name)
            if url:
                updates.append("url = ?")
                params.append(url)
            if ingredients:
                updates.append("ingredients = ?")
                params.append("\n".join(ingredients))
            if instructions:
                updates.append("instructions = ?")
                params.append("\n".join(instructions))
            if categories:
                updates.append("categories = ?")
                params.append(", ".join(categories))
            params.append(recipe_id)
            query = f"UPDATE recipes SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, tuple(params))
            self.connection.commit()
            print(f"Recipe with ID {recipe_id} updated.")

    def search_recipes(self, query):
        """Search for recipes by name or categories."""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                SELECT * FROM recipes
                WHERE name LIKE ? OR categories LIKE ?
            """, (f"%{query}%", f"%{query}%"))
            return cursor.fetchall()