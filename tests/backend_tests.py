import unittest
from unittest.mock import patch, Mock
import sqlite3
from guthub.recipe import Recipe
from guthub.database import Database


class TestRecipe(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.connection = sqlite3.connect(":memory:")
        self.db = Database(connection=self.connection)

    def tearDown(self):
        # Close the in-memory database
        self.connection.close()

    @patch(f'{Recipe.__module__}.requests.get')
    def test_get_recipe(self, mock_get):
        # Mock HTML content
        mock_html = '''
        <html>
            <body>
                <div class="ingredient">1 cup flour</div>
                <div class="ingredient">2 eggs</div>
                <div class="instruction">Mix ingredients</div>
                <div class="instruction">Bake at 350°F for 20 minutes</div>
            </body>
        </html>
        '''
        # Configure the mock to return a response with the mock HTML
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        # Create a Recipe instance and call get_recipe
        recipe = Recipe("http://example.com/recipe")
        recipe.get_recipe()

        # Validate the extracted data using to_dict
        recipe_data = recipe.to_dict()
        self.assertEqual(recipe_data["ingredients"], ["1 cup flour", "2 eggs"])
        self.assertEqual(recipe_data["instructions"], ["Mix ingredients", "Bake at 350°F for 20 minutes"])

    def test_save_recipe_to_db(self):
        # Create a sample recipe
        recipe = Recipe("https://www.example.com/sample-recipe")
        recipe.name = "Sample Recipe"
        recipe.ingredients = ["1 cup sugar", "2 cups flour"]
        recipe.instructions = ["Mix ingredients", "Bake at 350°F for 30 minutes"]
        recipe.categories = ["Dessert", "Baking"]

        # Save the recipe to the database
        self.db.save_recipe(
            name=recipe.name,
            url=recipe.url,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            categories=recipe.categories
        )

        # Verify the recipe was saved
        recipes = self.db.fetch_all_recipes()
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0][1], "Sample Recipe")


if __name__ == "__main__":
    unittest.main()
