from flask import Flask, render_template, request
from db import start_database
import sqlite3


app = Flask(__name__)
DATABASE = "recipes.db"

def get_all_recipes():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT title, ingredients, url FROM recipes")
    rows = cursor.fetchall()
    conn.close()

    recipes = []
    for row in rows:
        recipes.append({
            "title": row[0],
            "ingredients": [ingredient.strip().lower() for ingredient in row[1].split(",")],
            "url": row[2]
        })
    return recipes

@app.route("/", methods=["GET", "POST"])
def index():
    recipes_found = []
    partial_recipes = []
    recipes_with_extra = []
    user_ingredients = []

    if request.method == "POST":
        user_ingredients = request.form.get("ingredients", "").lower().strip()
        user_ingredients = [ingredient.strip() for ingredient in user_ingredients.split(",")]

        all_recipes = get_all_recipes()

        for recipe in all_recipes:
            recipe_ingredients = recipe["ingredients"]

            if set(recipe_ingredients).issubset(user_ingredients): #Полное совпадение
                recipes_found.append({
                    "title": recipe["title"],
                    "ingredients": ", ".join(recipe["ingredients"]),
                    "url": recipe["url"]
                })

            elif set(user_ingredients).intersection(recipe_ingredients): #Частичное совпадение
                partial_recipes.append({
                    "title": recipe["title"],
                    "ingredients": ", ".join(recipe["ingredients"]),
                    "url": recipe["url"]
                })

    return render_template(
        "index.html",
        recipes_found=recipes_found,
        partial_recipes=partial_recipes,
        user_ingredients=", ".join(user_ingredients)
    )

if __name__ == "__main__":
    start_database()
    app.run(host="0.0.0.0", port=5000)
