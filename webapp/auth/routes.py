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
            login_user(User(user), remember=True)

            # redirect to the product page
            return redirect(url_for("auth.home_page"))
        else:
            # If credentials is wrong flash a message
            flash('Credentials entered is incorrect. Create an account instead!', category='error')
    
    return render_template('login.html', navOptions= {'/register': 'Register'})

@auth.route('/register')
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
            # create a collection of the new user
            db.users.insert_one({"username": username, "password": password, "role": role, "products": []})

            # User is registered, save user details in session and remember user after session expires
            login_user(User(username, password, role, []), remember=True)

            # redirect to the product page
            return redirect(url_for("auth.home_page"))

            # flash('Registered succesfully!', category='success')

    return render_template('register.html', navOptions= {'/login': 'Login'})
