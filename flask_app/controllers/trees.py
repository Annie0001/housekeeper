from flask import Flask, render_template, request,redirect,session,flash
from flask_app import app
from flask_app.models.tree import Tree
from flask_app.models.user import User


@app.route('/show/<int:id>')
def show_tree(id):
    #checking if user is not in session then redirect to /
    if not session.get('user_id'):
        return redirect('/')
    
    data = {
        "id" : id
    }   
    tree_from_db = Tree.get_tree_by_id(data)

    return render_template('show_tree.html',tree = tree_from_db)


@app.route('/new/tree')
def show_new_tree():
    #checking if user is not in session then redirect to /
    if not session.get('user_id'):
        return redirect('/')
    
    return render_template('show_new_tree.html')

@app.route('/new', methods=['POST'])
def add_tree_to_db():

    if not Tree.validate_add_tree(request.form):
        return redirect('/new/tree')

    data={
            "species":request.form['species'],
            "location":request.form['location'],
            "reason":request.form['reason'],
            "date_planted":request.form['date_planted'],
            "user_id":request.form['user_id']
    }
    Tree.add_tree(data)

    return redirect ('/dashboard')

@app.route('/edit/<int:id>')
def show_edit_tree(id):
    #checking if user is not in session then redirect to /
    if not session.get('user_id'):
        return redirect('/')
    
    data = {
        "id" : id
    }
    tree_from_db = Tree.get_tree_by_id(data)
    return render_template('show_edit_tree.html',tree = tree_from_db)


@app.route('/edit/tree/<int:id>', methods=['POST'])
def update_tree(id):

    if not Tree.validate_add_tree(request.form):
        return redirect('/new')

    data={
            "id": id,
            "species":request.form['species'],
            "location":request.form['location'],
            "reason":request.form['reason'],
            "date_planted":request.form['date_planted'],
            "user_id":request.form['user_id']
    }
    Tree.update_tree(data)

    return redirect ('/user/account')


@app.route('/delete/<int:id>')
def delete_tree(id):

    data = {
        "id" : id
    }
    Tree.delete_tree_by_id(data)
    return redirect('/user/account')

@app.route('/visit/<int:id>')
def visit_tree(id):

    data = {
        "id" : id,
        "user_id": session['user_id']
    }
    tree_visitor_user = Tree.get_tree_visitor_by_user_id_and_tree_id(data)
    if not tree_visitor_user:
        Tree.visit_tree_by_user_id(data)
    return redirect('/show/'+ str(id))

