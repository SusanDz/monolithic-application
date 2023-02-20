from flask import Blueprint

order_page = Blueprint('order_page', __name__)

#import routes.py so registering time routes get registered as well
from webapp.order_page import routes