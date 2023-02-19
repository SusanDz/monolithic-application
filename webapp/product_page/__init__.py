from flask import Blueprint

product_page = Blueprint('product_page', __name__)

#import routes.py so registering time routes get registered as well
from webapp.product_page import routes