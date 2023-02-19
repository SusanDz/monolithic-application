from flask import render_template, request, flash, redirect, url_for
from webapp.product_page import product_page as product

@product.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        # get username and password from form
        username = request.form.get('username')
        password = request.form.get('password')

        print(username)

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
                # If username and password doesn't match flash message
                flash('Username or Password entered is incorrect.', category='error')
        else:
            # MIGHT REMOVE THIS CONDITION
            flash('Credentials entered is incorrect. Create an account instead!', category='error')

    return render_template('products.html')
