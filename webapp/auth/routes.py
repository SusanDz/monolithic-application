from flask import render_template
from webapp.auth import auth

@auth.route('/login')
def login():
    return render_template('base.html')

@auth.route('/signup')
def signup():
    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'