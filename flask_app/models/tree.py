from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Tree:
    def __init__( self , data ):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date_planted = data['date_planted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id= data['user_id']
        self.creator = None
        self.visitors_count = 0
        self.visitors = []

    @classmethod
    def get_trees_from_db(cls):
        query = "SELECT * FROM tree JOIN users ON tree.user_id = users.id"

        results = connectToMySQL('housekeeper_schema').query_db(query)

        print(results)

        trees = []

        if results:
            for row in results:
                # convert book data from row into object
                tree = cls(row)
                
                data = {
                    "id" : row['users.id'],
                    "first_name":row['first_name'],
                    "last_name":row['last_name'],
                    "email":row['email'],
                    "password":row['password'],
                    "created_at":row['users.created_at'],
                    "updated_at":row['users.updated_at'],
                }

                tree.creator = user.User(data)
                print(tree.creator)

                tree_visitor_data = {
                    "id": row['id']
                }
                tree_visitors = Tree.get_all_tree_visitors(tree_visitor_data)
                tree.visitors_count = len(tree_visitors)

                # add these books into all_books list
                trees.append(tree)
        return trees
    
    @classmethod
    def get_tree_by_id(cls,data):
        query = "SELECT * FROM tree JOIN users ON tree.user_id = users.id where tree.id=%(id)s"
        results = connectToMySQL('housekeeper_schema').query_db(query,data)

        row = results[0]
        user_data = {
                    "id" : row['users.id'],
                    "first_name":row['first_name'],
                    "last_name":row['last_name'],
                    "email":row['email'],
                    "password":row['password'],
                    "created_at":row['users.created_at'],
                    "updated_at":row['users.updated_at'],
        }


        tree = cls(row)
        tree.creator = user.User(user_data)

        # fill in visitors
        
        results_visitors = Tree.get_all_tree_visitors(data)
        print('results_visitors', results_visitors)
        if results_visitors:
            for row in results_visitors:
                user_data = {
                    "id" : row['users.id'],
                    "first_name":row['first_name'],
                    "last_name":row['last_name'],
                    "email":row['email'],
                    "password":row['password'],
                    "created_at":row['created_at'],
                    "updated_at":row['updated_at'],
                }
                user_visitor = user.User(user_data)
                tree.visitors.append(user_visitor)

        return tree
    
    @classmethod
    def get_all_tree_visitors(cls, data):
        query_visitors = "SELECT * FROM tree_visitor JOIN users ON tree_visitor.user_id = users.id where tree_visitor.tree_id=%(id)s"
        results_visitors = connectToMySQL('housekeeper_schema').query_db(query_visitors,data)
        return results_visitors

    @classmethod
    def add_tree(cls,data):
        query = "INSERT INTO tree (species, location, reason, date_planted, user_id) VALUES (%(species)s,%(location)s,%(reason)s,%(date_planted)s,%(user_id)s)"
        return connectToMySQL('housekeeper_schema').query_db(query,data)
    
    @classmethod
    def update_tree(cls,data):
        query = "UPDATE tree set species=%(species)s, location=%(location)s, reason=%(reason)s, date_planted=%(date_planted)s where id=%(id)s"
        return connectToMySQL('housekeeper_schema').query_db(query,data)
    

    @classmethod
    def get_trees_by_user_id(cls,data):
        query = "SELECT * FROM tree WHERE user_id = %(user_id)s"
        results = connectToMySQL('housekeeper_schema').query_db(query,data)
    
        trees = []

        if results:
            for row in results:
                # convert book data from row into object
                tree = cls(row)
                trees.append(tree)
        return trees

    @classmethod
    def delete_tree_by_id(cls,data):
        query = "delete from tree where id=%(id)s"
        return connectToMySQL('housekeeper_schema').query_db(query,data)
    

    @staticmethod
    def validate_add_tree(tree):
        is_valid = True

        # validations
        if len(tree["species"]) < 5:
            flash('Species should have at least 5 characters!!!', 'add_tree')
            is_valid = False
        if len(tree["location"]) < 2:
            flash('Location should have at least 2 characters!!!', 'add_tree')
            is_valid = False
        if not tree["reason"] or len(tree["reason"]) > 50:
            flash('Reason should have at most 50 characters!!!', 'add_tree')
            is_valid = False
        if not tree["date_planted"]:
            flash('Date Planted should be entered!!!', 'add_tree')
            is_valid = False

        return is_valid
    
    @classmethod
    def visit_tree_by_user_id(cls,data):
        query = "INSERT INTO tree_visitor (user_id, tree_id) VALUES (%(user_id)s,%(id)s)"
        return connectToMySQL('housekeeper_schema').query_db(query,data)
    
    @classmethod
    def get_tree_visitor_by_user_id_and_tree_id(cls,data):
        query = "SELECT * FROM tree_visitor WHERE user_id = %(user_id)s and tree_id=%(id)s"
        results = connectToMySQL('housekeeper_schema').query_db(query,data)
        return results
    

