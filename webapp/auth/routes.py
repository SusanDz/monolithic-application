from flask import render_template, request, session, flash, redirect, url_for
from webapp import db
# , login_manager
from ..models import User
from webapp.auth import auth
from flask_login import login_user, logout_user, login_required
# from flask_user import roles_required, login_required
# from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get username and password from form
        uname = request.form.get('username')
        passw = request.form.get('password')
        print(request.form.get('username'))

        # user is returned then the user with given username exists
        user = db.users.find_one({"username": uname, "password": passw})
        print(user)
        # user = db.Product.users.find_one({"username": request.form.get('uname'), "password":  request.form.get('passw')})
        # user  = User(username=uname, password=passw)

        if user:
            # session["username"] = user["username"]
            # session["role"] = user["role"]

            # User is logged in, sture user details in session and remember user even after session expires
            login_user(User(_id=user['_id'], username=user['username'], password=user['password'], role=user['role'], products=user['products']))

            # redirect to the product page
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

        # user is returned then the user with given username exists
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
    return redirect(url_for('login'))

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