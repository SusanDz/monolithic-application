from flask import render_template, request, flash, redirect, url_for
from webapp.order_page import order_page as order

@order.route('/order', methods=['GET', 'POST'])
def order():
    #get data from send as variable key value pair
    return render_template('order.html')
