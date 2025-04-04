import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_all_recipes(client):
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Should return a list of recipes


def test_add_new_recipe(client):
    new_recipe = {
        "title": "Salad",
        "ingredients": ["Lettuce", "Tomato", "Cucumber"],
        "cuisine": "Mediterranean",
        "youtube_link": "https://youtube.com/salad_recipe",
    }

    response = client.post("/recipes", json=new_recipe)
    assert response.status_code == 201
    assert response.json["message"] == "Recipe added successfully"


def test_update_recipe(client):
    updated_recipe = {
        "ingredients": ["Lettuce", "Tomato", "Olives"],  # Updated ingredient
        "cuisine": "Mediterranean",
        "youtube_link": "https://youtube.com/salad_updated",
    }

    response = client.put("/recipes/Salad", json=updated_recipe)
    assert response.status_code == 200
    assert response.json["message"] == "Recipe updated successfully"


def test_get_recipe_by_title(client):
    # Assuming a recipe with title 'Salad' exists in the cookbook.json
    response = client.get("/recipes/Salad")
    assert response.status_code == 200
    assert response.json["title"] == "Salad"  # Adjust according to sample data


def test_delete_recipe(client):
    response = client.delete("/recipes/Salad")
    assert response.status_code == 200
    assert response.json["message"] == "Recipe deleted successfully"


def test_add_recipe_missing_fields(client):
    incomplete_recipe = {
        "title": "Soup",
        "ingredients": ["Tomato", "Onion"],
        # Missing 'cuisine' and 'youtube_link'
    }

    response = client.post("/recipes", json=incomplete_recipe)
    assert response.status_code == 400
    assert response.json["error"] == "Missing fields"


def test_add_recipe_already_exists(client):
    existing_recipe = {
        "title": "Pasta",
        "ingredients": ["Tomato", "Basil", "Garlic"],
        "cuisine": "Italian",
        "youtube_link": "https://youtube.com/pasta_recipe",
    }

    response = client.post("/recipes", json=existing_recipe)
    assert response.status_code == 400
    assert response.json["error"] == "Recipe already exists"


def test_get_recipe_not_found(client):
    response = client.get("/recipes/NonExistentRecipe")
    assert response.status_code == 404
    assert response.json["error"] == "Recipe not found"
