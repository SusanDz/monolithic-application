from flask import render_template, request, session, flash, redirect, url_for
from pydantic import ValidationError
from ..models import mongo, User
from webapp.auth import auth
from flask_login import login_user, logout_user
import json

db = mongo.db

#login() is a View function that handles application routes for the URLs '/' and '/login'
@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get username and password from form
        uname = request.form.get('username')
        passw = request.form.get('password')
        print(request.form.get('username'))

        # convert application form data to json format
        form_data = json.dumps(request.form.to_dict())
        json_form = json.loads(form_data)

        # Validate the data to set of constraints set
        try:
            User(**json_form)
        except ValidationError as e:
            error_messages = [f"{error['loc']}: {''.join(error['msg'])}" for error in e.errors()]
            flash('Validation error: ' + ', '.join(error_messages), category='error')
            return redirect(url_for('auth.login'))

        # if user is returned then the user with given username exists
        user = db.users.find_one({"username": uname, "password": passw})
        print(user)

        if user:
            # User is logged in, sture user details in session and remember user even after session expires
            login_user(User(_id=user['_id'], username=user['username'], password=user['password'], role=user['role'], products=user['products']))

            # redirect to the product page
            # URL reversing function 'url_for'builds a URL to a specific function
            return redirect(url_for("product_page.products"))
        else:
            # If credentials is wrong flash a message
            flash('Credentials entered is incorrect. Create an account instead!', category='error')
    
    return render_template('login.html', navOptions= {'/register': 'Register'})

@auth.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get username, email, password and role from form
        username = request.form.get('username')
        # email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        print(role)

        # Check if username already taken
        user = db.users.find_one({"username": username})

        if user:
            # flash message for already exisiting username
            flash('This username has already been taken.', category='error')
        elif(len(password)<8):
            flash('Length of the password needs to be greater than 8', category='error')
        elif(not(user)):
            # create a new document of the new user
            db.users.insert_one({"username": username, "password": password, "role": role, "products": []})

            # get user record id
            id = getUserId(username)

            # User is registered, save user details in session and remember user after session expires
            login_user(User(id, username, password, role, []))

            # redirect to the product page
            return redirect(url_for("product_page.products"))

            # flash('Registered succesfully!', category='success')

    return render_template('register.html', navOptions= {'/login': 'Login'})

@auth.route('/logout')
def logout():
    #log out the user 
    logout_user()

    # flash success message
    flash('Logged out successfully!')
    
    return redirect(url_for('auth.login'))

# Define a decorator function that checks the user's role
def role_required(allowed_roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if session.get("role") not in allowed_roles:
                return redirect(url_for("auth.logout"))
            return func(*args, **kwargs)
        return wrapper
    return decorator

def getUserId(username):
    user = db.users.find_one({"username": username})
    return user['_id']