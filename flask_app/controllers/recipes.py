from flask_app import app
from flask import get_flashed_messages, render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route("/recipes/new")
def create_recipe():
    if "user_id" not in session:
        return redirect("/logout")
    return render_template("create.html", messages = get_flashed_messages())

@app.route("/recipes/save", methods=['POST'])
def save_recipe():
    if "user_id" not in session:
        return redirect("/logout")
    if not Recipe.validate_recipe(request.form):
        return redirect("/dashboard")
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "under_30_min": request.form["under_30_min"],
        "user_id": session["user_id"]
    }
    Recipe.create(data)
    return redirect("/dashboard")

@app.route("/recipes/<int:id>")
def view_instructions(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": id}
    this_user = User.get_user_by_id({"id": session["user_id"]})
    return render_template("recipe_instructions.html", this_user = this_user, recipe = Recipe.get_one(data))

@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": id}
    Recipe.delete(data)
    return redirect("/dashboard")

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": id}
    return render_template("edit_recipe.html", recipe = Recipe.get_one(data))

@app.route("/recipes/update", methods=["POST"])
def update_recipe():
    if "user_id" not in session:
        return redirect("/logout")
    if not Recipe.validate_recipe:
        return redirect("/dashboard")
    Recipe.update(request.form)
    return redirect("/dashboard")