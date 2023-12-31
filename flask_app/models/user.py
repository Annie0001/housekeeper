from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.rate = data ['rate']
        self.zip_code = data ['service_zip_code']
        self.phone_number = data ['phone_number']
        self.description = data['description']
        self.home = data ['home_service']
        self.office = data ['office_service']
        self.deep_cleaning = data ['deep_cleaning_service']
        self.same_day_cleaning = data ['same_day_cleaning_service']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.gender = data['gender']
        self.photo = data['photo']
    
    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email,password, is_housekeeper) VALUES(%(fname)s, %(lname)s, %(email)s , %(password)s , %(is_housekeeper)s);"

        return connectToMySQL('housekeeper_schema').query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"

        results =  connectToMySQL('housekeeper_schema').query_db(query,data) 
        # if user with this email does not exist, return false
        if len(results) < 1:
            return False
        
        #create class instance of user returned becasue the user exists with the given email
        user_from_db = cls(results[0])
        return user_from_db
    
    @classmethod
    def get_user_by_email_and_not_id(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s and id !=%(id)s"

        results =  connectToMySQL('housekeeper_schema').query_db(query,data) 
        # if user with this email does not exist, return false
        if len(results) < 1:
            return False
        
        #create class instance of user returned becasue the user exists with the given email
        user_from_db = cls(results[0])
        return user_from_db


    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"

        results =  connectToMySQL('housekeeper_schema').query_db(query,data) 
        # if user with this id does not exist, return false
        if len(results) < 1:
            return False
        
        #create class instance of user returned becasue the user exists with the given email
        user_from_db = cls(results[0])
        return user_from_db

    @classmethod
    def update_user(cls,data):
        query = """UPDATE users SET first_name=%(firstname)s,
        last_name=%(lastname)s,email=%(email)s WHERE id = %(id)s
        """
        return connectToMySQL('housekeeper_schema').query_db(query,data)
    

    @staticmethod
    def validate_user(user):
        is_valid = True

        # validation for first name field on registration form
        if len(user["firstname"]) < 3:
            flash('Your Name should have at least 3 characters!!!', 'registration')
            is_valid = False
        if not user["firstname"].isalpha():
            flash('Your Name should contain only letters!!!', 'registration')
            is_valid = False

        # validation for last name field on registration form
        if len(user["lastname"]) < 3:
            is_valid = False
            flash('Your Last Name should have at least 3 characters!!!','registration')
        if not user["lastname"].isalpha():
            flash('Your  Last Name should contain only letters!!!','registration')
            is_valid = False

        #validating email format
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'registration')
            is_valid = False
        
        #validation for email field on registration form
        #checking if email in the registration form exists in the database or not
        data = {
            "email":user["email"]
        }
        # getting user from database by email
        user_in_database = User.get_user_by_email(data)
        
        if user_in_database:
            flash('A user with the given email is already registered. Choose another email.', 'registration')
            is_valid = False

        # Checking the password length
        if len(user['password']) < 8:
            flash('Your password should have at least 8 characters!!!',  'registration')
            is_valid = False

        # confirm password and confrim password fields match
        if user['password'] != user['confPassword']:
            flash('Password and confirm Password do not match! Please enter it again.', 'registration')
            is_valid = False

        return is_valid
    
    

    @staticmethod
    def validate_user_on_edit(user):
        is_valid = True

        # validation for first name field on update_user
        if len(user["firstName"]) < 3:
            flash('Your Name should have at least 3 characters!!!', 'update_user')
            is_valid = False
        if not user["firstName"].isalpha():
            flash('Your Name should contain only letters!!!', 'update_user')
            is_valid = False

        # validation for last name field on update_user
        if len(user["lastName"]) < 3:
            is_valid = False
            flash('Your Last Name should have at least 3 characters!!!','update_user')
        if not user["lastName"].isalpha():
            flash('Your  Last Name should contain only letters!!!','update_user')
            is_valid = False

        #validating email format
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'update_user')
            is_valid = False
        
        #validation for email field on update_user
        #checking if email in the update_user exists in the database or not
        data = {
            "id": user["id"],
            "email":user["email"]
        }
        # getting user from database by email
        user_in_database = User.get_user_by_email_and_not_id(data)
        
        if user_in_database:
            flash('A user with the given email is already registered. Choose another email.', 'update_user')
            is_valid = False
    
        print("phone: ", user["phone_number"])

        # phone_number
        if not user["phone_number"].isnumeric():
            flash('Phone Number should contain only numbers!!!', 'update_user')
            is_valid = False
        if "phone_number" in user and len(user["phone_number"]) != 10:
            flash('Phone Number must contain 10 digits!!!', 'update_user')
            is_valid = False

        # zip code validation to be number
        if not user["zip_code"].isnumeric():
            flash('Zip Code should contain only numbers!!!', 'update_user')
            is_valid = False
        if len(user["zip_code"]) != 5:
            flash('Zip Code must contain 5 digits!!!', 'update_user')
            is_valid = False

        # rate validation to be number
        if not user["rate"].isnumeric():
            flash('Rate should contain only numbers!!!', 'update_user')
            is_valid = False
        if not user["rate"].isnumeric() or len(user["rate"]) < 1 or int(user["rate"]) < 1 or len(user["rate"]) > 3:
            flash('Rate must contain up to 3 digits and more than 1!!!', 'update_user')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_search_user(user):
        is_valid = True

        # zip code validation to be number
        if not user["zip_code"].isnumeric():
            flash('Zip Code should contain only numbers!!!', 'search_cleaning_services')
            is_valid = False
        if len(user["zip_code"]) != 5:
            flash('Zip Code must contain 5 digits!!!', 'search_cleaning_services')
            is_valid = False
        return is_valid

    @classmethod
    def housekeeper_search_results(cls,data):
        #query = "SELECT * FROM users where is_housekeeper = 1 and home_service=%(home)s and office_service=%(office)s and deep_cleaning_service=%(deep_cleaning)s and same_day_cleaning_service= %(same_day_cleaning)s and rate< %(rate)s and service_zip_code = %(zip_code)s"

        query = "SELECT * FROM users where is_housekeeper = 1 "

        if "home" in data:
            query += " and home_service=%(home)s"
        
        if "office" in data:
            query += " and office_service=%(office)s"
        
        if "deep_cleaning" in data:
            query += " and deep_cleaning_service=%(deep_cleaning)s"

        if "same_day_cleaning" in data:
            query += " and same_day_cleaning_service= %(same_day_cleaning)s"

        query += " and rate< %(rate)s and service_zip_code = %(zip_code)s"


        results =  connectToMySQL('housekeeper_schema').query_db(query,data)
        # if user with this email does not exist, return false

        print(results)
        housekeepers = []
        #create class instance of user returned becasue the user exists with the given email
        if results:
            for row in results:
                # convert book data from row into object
                user = cls(row)
                housekeepers.append(user)
        return housekeepers


    @classmethod
    def update_housekeeper_profile(cls, data):
        query = "Update users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, phone_number=%(phone_number)s, service_zip_code=%(zip_code)s, rate=%(rate)s, description=%(description)s, home_service=%(home_cleaning)s, office_service=%(office_cleaning)s, deep_cleaning_service=%(deep_cleaning_services)s, same_day_cleaning_service=%(same_day_cleaning_services)s, gender=%(gender)s where id=%(id)s"

        return connectToMySQL('housekeeper_schema').query_db(query, data)
    
    @classmethod
    def housekeeper_file_upload(cls, data):
        query = "UPDATE users SET photo= %(file_name)s where id = %(user_id)s"

        return connectToMySQL('housekeeper_schema').query_db(query, data)
    
    
    