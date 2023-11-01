from flask import Flask, render_template, request,redirect,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.skill import Skill

@app.route('/housekeeper_profile/<int:id>/skill/add')
def show_add_skills(id):

    data={
        "user_id":id

    }
    housekeeper_from_db = User.get_user_by_id(data)

    return render_template('skills.html', housekeeper_for_add_skills = housekeeper_from_db  )
    
@app.route('/housekeeper_profile/<int:id>/add_skill',methods=['POST'])
def add_skills(id):
    
    data = {
        "user_id":id,
        "skills_description": request.form["skills_name"]
    }
    Skill.add_skills_from_db(data)
    return redirect('/housekeeper_profile/' + str(id) +'/profile/show_edit')

@app.route('/housekeeper_profile/<int:id>/skill/<int:skill_id>/show_update_skill')
def show_update_skills(id,skill_id):

    data={
        "user_id":id

    }
    housekeeper_from_db = User.get_user_by_id(data)
    return render_template('update_skills.html',housekeeper_for_add_skills = housekeeper_from_db )
