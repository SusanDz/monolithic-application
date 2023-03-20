from flask import render_template, request, flash, redirect, url_for
from webapp.product_page import product_page as product

@product.route('/products', methods=['GET', 'POST'])
def products():
    #get products from db and send to to html
    return render_template('products.html')

@product.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'POST':
        # get name and price and picture from form
        name = request.form.get('name')
        price = request.form.get('price')
        picture = request.form.get('picture')

        flash('Created product succesfully!', category='success')
        
    return render_template('addProduct.html')