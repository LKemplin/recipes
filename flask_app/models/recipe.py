from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db = "recipes"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.under_30_min = data["under_30_min"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        print("***********************", recipes)
        return recipes
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30_min, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30_min)s, %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results

    @staticmethod
    def validate_recipe(recipe_form):
        is_valid = True
        if len(recipe_form["name"]) < 3:
            flash("Please enter a recipe name longer than 3 characters.")
            is_valid = False
        if len(recipe_form["description"]) < 3:
            flash("Please enter a recipe description longer than 3 characters.")
            is_valid = False
        if len(recipe_form["instructions"]) < 3:
            flash("Please enter recipe instructions longer than 3 characters.")
            is_valid = False
        if len(recipe_form["date_made"]) < 1:
            flash("Please enter the date you made this recipe.")
            is_valid = False
        # if recipe_form["under_30_min"] is None:
        #     flash("Please choose whether your recipe is under 30 minutes.")
        #     is_valid = False
        return is_valid

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30_min = %(under_30_min)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
