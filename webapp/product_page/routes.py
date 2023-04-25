from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from webapp.product_page import product_page as product
from .. import db

@product.route('/products', methods=['GET'])
@login_required
def products():
    #get products from db and send to html
    products = db.products.find()

    #get list of products from collection
    productls = []
    for product in products:
        productls.append({'name': product['name'], 'price': product['price'], 'img': product['picture']})

    #depending on user role display fifferent navbar options
    navBarOps = {}
    if(current_user.role == 'Customer'):
        navBarOps = {'/order': 'Shopping Cart'}
    elif(current_user.role == 'Product Owner'):
        navBarOps = {'/addProduct': 'Add Products'}
    print(current_user.role)
    
    return render_template('products.html', products = productls, navOptions= navBarOps)

@product.route('/addProduct', methods=['GET', 'POST'])
@login_required
def addProduct():
    if request.method == 'POST':
        # get name and price and picture from form
        name = request.form.get('name')
        price = request.form.get('price')
        picture = request.form.get('picture')

        # create a new product document
        product_doc = {
            'name': name,
            'price': price,
            'picture': picture
        }

        # insert the product document to the database
        db.products.insert_one(product_doc)

        # send a flash message to screen with success message
        flash('Created product succesfully!', category='success')
        
    return render_template('addProduct.html', navOptions= {'/products': 'Products'})