from flask import Flask, render_template, request,redirect,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.tree import Tree

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def show_registeration_and_login():

    return render_template('create.html')

@app.route('/register_user', methods=['POST'])
def register_user():

    # checking the submitted registeration form fields are valid or not 
    if not User.validate_user(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    
    data={
        "fname":request.form["firstname"],
        "lname":request.form["lastname"],
        "email":request.form["email"],
        "password":pw_hash
    }
    User.register(data)

    # getting user by email from db, so that we put the user id in session
    user_in_db = User.get_user_by_email(data)

    # saving user first name in session
    session['fname']=request.form["firstname"]
    #we need to put user id in session
    session['user_id']=user_in_db.id

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') # redirect to register page again

@app.route('/login' , methods=['POST'])
def login():
    data = {
        "email":request.form["login_email"]
    }
    #checking if user with a given email exists in the database
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", 'Login')
        return redirect('/')
    
    #if we reach this line it means the user with the given email exists in the db
    # checking if given password is equal to the password hashed in db
    password_matches = bcrypt.check_password_hash(user_in_db.password, request.form["password"])
    if not password_matches:
        flash("Invalid Email/Password", 'Login')
        return redirect('/')

    # If we reach this step, this means login email and password is correct and exists in the database
    # saving user first name in session
    session['fname']=user_in_db.first_name
    session['user_id']=user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    #checking if user is not in session then redirect to /
    if not session.get('user_id'):
        return redirect('/')
    
    trees_from_database = Tree.get_trees_from_db()
    return render_template('dashboard.html', trees = trees_from_database) 

@app.route('/user/account')
def show_account():
    #checking if user is not in session then redirect to /
    if not session.get('user_id'):
        return redirect('/')
    
    data = {
        "user_id" : session['user_id']
    }
    my_trees_from_db = Tree.get_trees_by_user_id(data)
    return render_template('show_account.html',trees = my_trees_from_db)

@app.route('/user/<int:id>', methods=['POST'])
def update_user(id):

    data = {
        "id" : id,
        "firstname":request.form["firstname"],
        "lastname":request.form["lastname"],
        "email":request.form["email"]
    }

    # validate
    if not User.validate_user_on_edit(data):
        return redirect('/user/account')

    User.update_user(data)
    return redirect('/user/account')




