from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from webapp.product_page import product_page as product
from bson.objectid import ObjectId
from pymongo import errors
import base64
from .. import db

# Display all products in database and navBar options according to user-role
@product.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    #get products from db and send to html
    products = db.products.find()

    #get list of products from collection
    productls = list(products)
    # for product in productls:
    #     print(product['_id'])

    #depending on user role display different navbar options
    navBarOps = {}
    if(current_user.role == 'Customer'):
        navBarOps = {'/order': 'Shopping Cart', '/logout': 'Log Out'}
    elif(current_user.role == 'Product Owner'):
        navBarOps = {'/addProduct': 'Add Products', '/logout': 'Log Out'}
    print(current_user.role)
    
    return render_template('products.html', products = productls, navOptions= navBarOps)

# Product Owner provides product details, insert record into Products collection in db
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
        product = db.products.insert_one(product_doc)

        # get id of product recently added
        pid = product.inserted_id

        # append product to user record
        db.users.update_one({'username': current_user.username}, {"$push": {'products': pid}})

        # send a flash message to screen with success message
        flash('Created product succesfully!', category='success')
        
    return render_template('addProduct.html', navOptions= {'/products': 'Products', '/logout': 'Log Out'})

# Customer adds product to cart, insert product id to the users orderProducts list
@product.route('/addProductToCart', methods=['POST'])
def handle_button_click():
    # get id and name of prduct to be added to cart
    productId = request.get_json()['id']
    productName = request.get_json()['name']

    # add product id to current user products list
    try:
        result = db.users.update_one({"username": current_user.username}, {"$push": {"products": ObjectId(productId) }})

        # if update sucessful send a success message
        if result.matched_count == 1 and result.modified_count == 1:
            return {'message': 'Sucess, Added '+productName+' to your cart!',  'category':'success'}

    except (errors.PyMongoError, AttributeError) as e:   
        # if error occured send a error message
        return {'message': 'Failed to add '+productName+' to your cart!',  'category':'danger'}

# get product id by searching for product by name and price
def getProductId(name, price):
    prod = db.products.find_one({"name": name, "price": price})
    return prod['_id']