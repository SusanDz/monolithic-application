from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from webapp.order_page import order_page as order

@order.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    data = []
    if request.method == 'POST':
        data = []
    else:
        #get data from send as variable key value pair
        data = [{'_id': 1, 'name': 'Banana', 'price': 15}, {'_id': 2, 'name': 'Pie', 'price': 15}]
    return render_template('order.html', data=data, navOptions= {'/products': 'Products'})
