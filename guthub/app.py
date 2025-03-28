from flask import Flask, render_template, request, redirect
from guthub.database import Database

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

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    name = request.form["name"]
    url = request.form["url"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    db.save_recipe(name, url, ingredients.split("\n"), instructions.split("\n"), [])
    return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    recipes = db.search_recipes(query)
    return render_template("search_results.html", recipes=recipes, query=query)

if __name__ == "__main__":
    app.run(debug=True)