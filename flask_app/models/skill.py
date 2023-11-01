from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Skill:
    def __init__( self , data ):
        self.id = data['id']
        self.skill_name = data['skill_name']
        self.user_id= data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def add_skills_from_db(cls,data):

        query = "INSERT INTO skill (skill_name, user_id) VALUES (%(skills_description)s, %(user_id)s)"
        
        results = connectToMySQL('housekeeper_schema').query_db(query,data)

    @classmethod
    def get_skills_from_db(cls,data):

        query = "SELECT * FROM skill WHERE user_id = %(user_id)s"

        results = connectToMySQL('housekeeper_schema').query_db(query,data)

        housekeeper_skills_list =[]

        if results:
            for row in results:
                # convert book data from row into object
                skill = cls(row)
                housekeeper_skills_list.append(skill)
        return housekeeper_skills_list

