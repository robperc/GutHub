from flask import Flask, render_template, request, redirect
from guthub.database import Database
from guthub.recipe import Recipe
import logging

logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

# Initialize the database
db = Database("recipes.db")

@app.route("/")
def home():
    recipes = db.fetch_all_recipes()  # Fetch all recipes from the database
    return render_template("index.html", recipes=recipes)

@app.route("/recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = db.fetch_recipe_by_id(recipe_id)
    return render_template("recipe.html", recipe=recipe)

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        # Process the form submission
        name = request.form["name"]
        url = request.form["url"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        categories = request.form.get("categories", "").split(",")  # Split categories by commas
        categories = [category.strip() for category in categories]  # Remove extra whitespace
        db.save_recipe(name, url, ingredients.split("\n"), instructions.split("\n"), categories)
        
        # Fetch the newly created recipe's ID
        recipe = db.fetch_recipe_by_name(name)
        return redirect(f"/recipe/{recipe[0]}")  # Redirect to the recipe's page
    # Render the form for GET requests
    return render_template("add_recipe.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    recipes = db.search_recipes(query)
    return render_template("search_results.html", recipes=recipes, query=query)

@app.route("/fetch_recipe_details")
def fetch_recipe_details():
    url = request.args.get("url", "").strip()
    if not url:
        return {"error": "URL is required"}, 400

    try:
        recipe = Recipe(url)
        recipe.get_recipe()
        return {
            "name": recipe.name,
            "ingredients": recipe.ingredients,
            "instructions": recipe.instructions,
            "categories": recipe.categories,  # Include categories if available
        }
    except Exception as e:
        logging.exception("Error fetching recipe details")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)