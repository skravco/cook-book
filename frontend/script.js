const API_URL = "https://cook-book-jagr.onrender.com/recipes";

// Fetch and display recipes
async function fetchRecipes() {
    const response = await fetch(API_URL);
    const recipes = await response.json();
    const container = document.getElementById("recipes-container");
    container.innerHTML = "";

    recipes.forEach(recipe => {
        const div = document.createElement("div");
        div.classList.add("recipe");
        div.innerHTML = `
            <h3>${recipe.title}</h3>
            <p><strong>Ingredients:</strong> ${recipe.ingredients.join(", ")}</p>
            <p><strong>Cuisine:</strong> ${recipe.cuisine}</p>
            <p><a href="${recipe.youtube_link}" target="_blank">Watch on YouTube</a></p>
            <button onclick="fillForm('${recipe.title}')">Edit</button>
            <button class="delete" onclick="deleteRecipe('${recipe.title}')">Delete</button>
        `;
        container.appendChild(div);
    });
}

// Add or update a recipe
async function addOrUpdateRecipe() {
    const title = document.getElementById("title").value;
    const ingredients = document.getElementById("ingredients").value.split(",");
    const cuisine = document.getElementById("cuisine").value;
    const youtube_link = document.getElementById("youtube_link").value;

    const response = await fetch(`${API_URL}/${title}`);
    const existingRecipe = response.status !== 404;

    const method = existingRecipe ? "PUT" : "POST";
    const url = existingRecipe ? `${API_URL}/${title}` : API_URL;

    const responseData = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, ingredients, cuisine, youtube_link }),
    });

    if (responseData.ok) {
        fetchRecipes();
        clearForm();
    }
}

// Fill form with existing recipe data
async function fillForm(title) {
    const response = await fetch(`${API_URL}/${title}`);
    if (response.ok) {
        const recipe = await response.json();
        document.getElementById("title").value = recipe.title;
        document.getElementById("ingredients").value = recipe.ingredients.join(", ");
        document.getElementById("cuisine").value = recipe.cuisine;
        document.getElementById("youtube_link").value = recipe.youtube_link;
    }
}

// Delete a recipe
async function deleteRecipe(title) {
    const response = await fetch(`${API_URL}/${title}`, { method: "DELETE" });

    if (response.ok) {
        fetchRecipes();
    }
}

// Clear the form
function clearForm() {
    document.getElementById("title").value = "";
    document.getElementById("ingredients").value = "";
    document.getElementById("cuisine").value = "";
    document.getElementById("youtube_link").value = "";
}

// Load recipes on page load
fetchRecipes();

