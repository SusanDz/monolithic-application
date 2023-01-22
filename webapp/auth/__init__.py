from flask import Blueprint

auth = Blueprint('auth', __name__)

#import routes.py so registering time routes get registered as well
from webapp.auth import routes