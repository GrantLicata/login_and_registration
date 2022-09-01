from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

# Validation schematics
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self ,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.gender = data['gender']
        self.language = data['language']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('user_login').query_db(query)
        data = []
        for item in results:
            data.append( cls(item) )
        return data

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, birthday, gender, language ,created_at, updated_at) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, %(birthday)s, %(gender)s, %(language)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('user_login').query_db( query, data )

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("user_login").query_db(query,data)
        # Didn't find a matching user
        print("-------- Result is:", result)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(data):
        is_valid = True # we assume this is true
        if len(data['first_name']) < 1:
            flash("First name is required.")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last name is required.")
            is_valid = False
        if len(data['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if len(data['birthday']) < 1:
            flash("Birthday is required.")
            is_valid = False
        if len(data['gender']) < 1:
            flash("Gender is required.")
            is_valid = False
        if len(data['language']) < 1:
            flash("Language is required.")
            is_valid = False
        return is_valid


    @staticmethod
    def validate_password(passwords):
        is_valid = True # we assume this is true
        if passwords['password'] != passwords['confirm_password']:
            flash("Passwords must be the same.")
            is_valid = False
        return is_valid