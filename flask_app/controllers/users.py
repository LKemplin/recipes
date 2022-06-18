from email import message
from flask_app import app
from flask import get_flashed_messages, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html", messages=get_flashed_messages())

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_user(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    session["user_id"] = User.create(data)
    print("*************************", session["user_id"])
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/logout")
    this_user = User.get_user_by_id({"id": session["user_id"]})
    return render_template("dashboard.html", this_user = this_user, recipes = Recipe.get_all())

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    this_user = User.get_by_email({"email": request.form['email']})
    if this_user:
        if bcrypt.check_password_hash(this_user.password, request.form["password"]):
            session["user_id"] = this_user.id
            return redirect("/dashboard")
    flash("Invalid Email/Password Combination")
    return redirect("/")

