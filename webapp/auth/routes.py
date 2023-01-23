from flask import render_template, request, flash, redirect, url_for
from models import User
from werkzeug.security import check_password_hash
from webapp.auth import auth
from flask_login import login_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get username and password from form
        username = request.form.get('username')
        password = request.form.get('password')

        # user is returned then the user with given username exists
        user = User.query.filter_by(username=username).first()

        if user:
            # for particular user check if the password provided matches with user in database
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')

                # User is logged in, remember user even after session expires
                login_user(user, remember=True)

                # redirect to function home of the route '/home'
                return redirect(url_for('profile.home'))
            else:
                flash('Password entered is incorrect.', category='error')
        else:
            flash('Email provided is incorrect.', category='error')

    return render_template('login.html')

@auth.route('/register')
def signup():
    return render_template('register.html')

@auth.route('/logout')
def logout():
    return 'Logout'