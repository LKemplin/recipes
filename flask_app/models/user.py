from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "recipes"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address")
            is_valid = False
        if request.form["password"] != request.form["confirm_password"]:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_user = cls(results[0])
        return this_user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        this_user = cls(results[0])
        return this_user