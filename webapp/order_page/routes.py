from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from webapp.order_page import order_page as order
from .. import db

@order.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    data = []
    if request.method == 'POST':
        data = []
    else:
        # get list of product ids from the user's products array field
        product_ids = db.users.find_one({'username': current_user.username})['products']

        # Using list comprehension fetch product details from 'products' collection
        pdata = [
            {
                'id': str(product['_id']),
                'name': product['name'],
                'price': product['price']
            }
            for pid in product_ids
            # Allow variable assignments (:=) within an exp
            if (product := db.products.find_one({'_id': pid}))
        ]

    #get data from send as variable key value pair
    data = [{'id': 1, 'name': 'Banana', 'price': 15}, {'_id': 2, 'name': 'Pie', 'price': 15}]
    return render_template('order.html', data=pdata, navOptions= {'/products': 'Products'})

# /order logic for getting product details without list comprehension
# pdata = []
# # Fetch each product's details from the 'products' collection
# for pid in product_ids:
#     product = db.products.find_one({'_id': pid})
#     product_data = {
#         'id': str(product['_id']),
#         'name': product['name'],
#         'price': product['price']
#     }
#     pdata.append(product_data)
#     print(pdata)