from flask import Flask, request, jsonify
from flask_cors import CORS 
import json
import os

app = Flask(__name__)

# CORS(app)
CORS(app, resources={r"/*": {"origins": "https://cook-book-gui.onrender.com"}})

DATA_FILE = "cookbook.json"

# Load data from JSON file
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/recipes", methods=["GET"])
def get_recipes():
    return jsonify(load_data())

@app.route("/recipes/<string:title>", methods=["GET"])
def get_recipe(title):
    recipes = load_data()
    recipe = next((r for r in recipes if r["title"].lower() == title.lower()), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({"error": "Recipe not found"}), 404

@app.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.json
    recipes = load_data()

    if not all(key in data for key in ["title", "ingredients", "cuisine", "youtube_link"]):
        return jsonify({"error": "Missing fields"}), 400

    if any(r["title"].lower() == data["title"].lower() for r in recipes):
        return jsonify({"error": "Recipe already exists"}), 400

    recipes.append(data)
    save_data(recipes)
    return jsonify({"message": "Recipe added successfully"}), 201

@app.route("/recipes/<string:title>", methods=["PUT"])
def update_recipe(title):
    data = request.json
    recipes = load_data()

    for recipe in recipes:
        if recipe["title"].lower() == title.lower():
            recipe.update(data)
            save_data(recipes)
            return jsonify({"message": "Recipe updated successfully"})

    return jsonify({"error": "Recipe not found"}), 404

@app.route("/recipes/<string:title>", methods=["DELETE"])
def delete_recipe(title):
    recipes = load_data()
    updated_recipes = [r for r in recipes if r["title"].lower() != title.lower()]

    if len(updated_recipes) == len(recipes):
        return jsonify({"error": "Recipe not found"}), 404

    save_data(updated_recipes)
    return jsonify({"message": "Recipe deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)

