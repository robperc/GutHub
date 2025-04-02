from flask import Flask, render_template, request, redirect, g
from guthub.database import Database
from guthub.recipe import Recipe
import logging

# logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app with updated template folder
app = Flask(__name__, template_folder="../templates")

def get_db():
    """Get or create a database connection for the current request."""
    if "db" not in g:
        g.db = Database()
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.connection.close()

@app.route("/")
def home():
    db = get_db()
    recipes = db.fetch_all_recipes()  # Fetch all recipes from the database
    return render_template("index.html", recipes=recipes)

@app.route("/recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    db = get_db()
    recipe = db.fetch_recipe_by_id(recipe_id)
    return render_template("recipe.html", recipe=recipe)

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    db = get_db()
    if request.method == "POST":
        # Process the form submission
        name = request.form["name"]
        url = request.form["url"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        categories = request.form.get("categories", "").split(",")
        categories = [category.strip() for category in categories]

        # Save the recipe to the database
        db.save_recipe(
            name=name,
            url=url,
            ingredients=ingredients.split("\n"),
            instructions=instructions.split("\n"),
            categories=categories
        )
        recipe = db.fetch_recipe_by_name(name)
        return redirect(f"/recipe/{recipe[0]}")  # Redirect to the recipe's page
    # Render the form for GET requests
    return render_template("add_recipe.html")

@app.route("/search")
def search():
    db = get_db()
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
        return recipe.to_dict()  # Use the to_dict method
    except Exception as e:
        logging.exception("Error fetching recipe details")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)