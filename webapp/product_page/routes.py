from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from webapp.product_page import product_page as product
import base64
from .. import db

@product.route('/products', methods=['GET'])
@login_required
def products():
    #get products from db and send to html
    products = db.products.find()

    #get list of products from collection
    productls = list(products)
    # for product in products:
    #     productls.append({'name': product['name'], 'price': product['price'], 'img': product['picture']})

    #depending on user role display fifferent navbar options
    navBarOps = {}
    if(current_user.role == 'Customer'):
        navBarOps = {'/order': 'Shopping Cart', '/logout': 'Log Out'}
    elif(current_user.role == 'Product Owner'):
        navBarOps = {'/addProduct': 'Add Products', '/logout': 'Log Out'}
    print(current_user.role)
    
    return render_template('products.html', products = productls, navOptions= navBarOps)

@product.route('/addProduct', methods=['GET', 'POST'])
@login_required
def addProduct():
    if request.method == 'POST':
        # get name and price and picture from form
        name = request.form.get('productName')
        price = request.form.get('productPrice')
        picture = request.files['productPic']

        print(name, price, picture)

         # convert the image to base64
        if picture:
            image_bytes = picture.read()
            b64 = base64.b64encode(image_bytes).decode('utf-8')
        else:
            b64 = None
        
        # create a new product document
        product_doc = {
            'name': name,
            'price': price,
            'picture': "data:image/jpeg;base64,"+b64
        }

        # insert the product document to the database
        db.products.insert_one(product_doc)

        # get id of product recently added
        pid = getProductId(name, price)

        # append product to user record
        db.users.update_one({'username': current_user.username}, {"$push": {'products': pid}})

        # send a flash message to screen with success message
        flash('Created product succesfully!', category='success')
        
    return render_template('addProduct.html', navOptions= {'/products': 'Products', '/logout': 'Log Out'})

# get product id by searching for product by name and price
def getProductId(name, price):
    prod = db.products.find_one({"name": name, "price": price})
    return prod['_id']