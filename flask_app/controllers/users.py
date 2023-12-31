from flask import Flask, render_template, request,redirect,session,flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.skill import Skill
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# To upload file/photo
UPLOAD_FOLDER = join(dirname(realpath(__file__)), '../static/Photos/uploads')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/housekeeper_profile/<int:id>/file_upload', methods=['GET','POST'])
def upload_file(id):
    if request.method == 'POST':
        print('upload_file POST')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'update_user')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'update_user')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # saving the file in the file system
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # saving the file_name in the database
            data = {
                "user_id": id,
                "file_name":filename
            }
            User.housekeeper_file_upload(data)
            return redirect('/housekeeper_profile/'+str(id)+'/profile/show_edit')
    
    print('upload_file NOT POST')
    return redirect('/housekeeper_profile/'+str(id)+'/profile/show_edit')


@app.route('/register_and_login')
def show_registeration_and_login():

    return render_template('register_and_login.html')

@app.route('/register_user', methods=['POST'])
def register_user():

    # checking the submitted registeration form fields are valid or not 
    if not User.validate_user(request.form):
        return redirect('/register_and_login')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    
    #     if "home" in request.form and request.form["home"] == "home_is_selected":

    is_housekeeper_value_checked = 0
    if "is_housekeeper" in request.form and request.form["is_housekeeper"] == "is_housekeeper_checked":
        print('entred if block')
        is_housekeeper_value_checked = 1


    print('request.form: ', request.form)
    data={
        "fname":request.form["firstname"],
        "lname":request.form["lastname"],
        "email":request.form["email"],
        "password":pw_hash,
        "is_housekeeper":is_housekeeper_value_checked
    }

    print('data:', data)
    User.register(data) 

    # getting user by email from db, so that we put the user id in session
    user_in_db = User.get_user_by_email(data)

    # saving user first name in session
    session['fname']=request.form["firstname"]
    #we need to put user id in session
    session['user_id']=user_in_db.id

    return redirect('/housekeeper_profile/'+str(user_in_db.id)+'/profile/show_edit')

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
    return redirect('/housekeeper_profile/'+str(user_in_db.id))

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

@app.route('/')
def index():

    return render_template('main.html')

@app.route('/cleaning_services')
def show_cleaning_services():
    return render_template('search_cleaning_services.html')

@app.route('/cleaning_services_search_results', methods=['POST'])
def search_cleaning_services_results():

    # checking the submitted registeration form fields are valid or not 
    if not User.validate_search_user(request.form):
        return redirect('/cleaning_services')

    # --------------------- THIS IS A SIMPLE SERACH> THIS IS COMMENTED TO DO ENHANCED SEARCH ----------------
    # home_value_check = 0
    # if "home" in request.form and request.form["home"] == "home_is_selected":
    #     home_value_check = 1
    
    # office_value_check = 0
    # if "office" in request.form and request.form["office"] == "office_is_selected":
    #     office_value_check = 1
    
    # deep_cleaning_value_check = 0
    # if "deep_cleaning" in request.form and request.form["deep_cleaning"] == "deep_cleaning_is_selected":
    #     deep_cleaning_value_check = 1

    # same_day_cleaning_value_check = 0
    # if "same_day_cleaning" in request.form and request.form["same_day_cleaning"] == "same_day_cleaning_is_selected":
    #     same_day_cleaning_value_check = 1

    # data = {
    #     "id" : id,
    #     "home":home_value_check,
    #     "office":office_value_check,
    #     "deep_cleaning":deep_cleaning_value_check,
    #     "same_day_cleaning": same_day_cleaning_value_check,
    #     "rate":request.form["rate"],
    #     "zip_code":request.form["zip_code"]
    # }

    #--------- ENHANCED SEARCH ------------------
    data = {
        "id" : id,
        "rate":request.form["rate"],
        "zip_code":request.form["zip_code"]
    }

    if "home" in request.form and request.form["home"] == "home_is_selected":
        data["home"] = 1
    
    if "office" in request.form and request.form["office"] == "office_is_selected":
        data["office"] = 1
    
    if "deep_cleaning" in request.form and request.form["deep_cleaning"] == "deep_cleaning_is_selected":
        data["deep_cleaning"] = 1

    if "same_day_cleaning" in request.form and request.form["same_day_cleaning"] == "same_day_cleaning_is_selected":
        data["same_day_cleaning"] = 1

    housekeepers_search_result = User.housekeeper_search_results(data)
    return render_template('search_cleaning_services.html', housekeepers =housekeepers_search_result)

@app.route('/housekeeper_profile/<int:id>')
def housekeeper_profile(id):
    data = {
        "user_id" : id
    }
    housekeeper_from_db = User.get_user_by_id(data)
    housekeeper_skills_form_db = Skill.get_skills_from_db(data)
    return render_template('housekeeper_profile.html', housekeeper = housekeeper_from_db, housekeeper_skills = housekeeper_skills_form_db)


@app.route('/housekeeper_profile/<int:id>/profile/show_edit')
def show_edit_housekeeper_profile(id):

    if not session.get('user_id'):
        return redirect('/')
    
    if id != session['user_id']:
        return redirect('/')

    data = {
        "user_id" : id
    }
    housekeeper_from_db = User.get_user_by_id(data)
    print('gender: ', housekeeper_from_db.gender)
    housekeeper_skills_form_db = Skill.get_skills_from_db(data)

    return render_template('edit_profile.html', housekeeper = housekeeper_from_db, housekeeper_skills = housekeeper_skills_form_db)

@app.route('/housekeeper_profile/<int:id>/profile/edit', methods=['POST'])
def edit_housekeeper_profile(id):

    if not User.validate_user_on_edit(request.form):
        print('entered here validate on edit')
        return redirect('/housekeeper_profile/' + str(id) + '/profile/show_edit')

    home_value_check = 0
    if "homeCleaning" in request.form and request.form["homeCleaning"] == "home":
        home_value_check = 1
    
    office_value_check = 0
    if "officeCleaning" in request.form and request.form["officeCleaning"] == "office":
        office_value_check = 1
    
    deep_cleaning_value_check = 0
    if "deepCleaning" in request.form and request.form["deepCleaning"] == "deep_cleaning":
        deep_cleaning_value_check = 1

    same_day_cleaning_value_check = 0
    if "sameDayCleaning" in request.form and request.form["sameDayCleaning"] == "same_day_cleaning":
        same_day_cleaning_value_check = 1

    data = {
        "id" : id,
        "first_name":request.form["firstName"],
        "last_name":request.form["lastName"],
        "email":request.form["email"],
        "phone_number":request.form["phone_number"],
        "zip_code":request.form["zip_code"],
        "rate":request.form["rate"],
        "description":request.form["description"],
        "home_cleaning":home_value_check ,
        "office_cleaning":office_value_check,
        "deep_cleaning_services":deep_cleaning_value_check,
        "same_day_cleaning_services":same_day_cleaning_value_check,
        "gender":request.form["genderOptions"]
    }

    User.update_housekeeper_profile(data)
    return redirect('/housekeeper_profile/' + str(id))
