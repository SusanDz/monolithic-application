from flask import Flask
from config import Config
from flask_login import LoginManager
from bson import ObjectId
import pymongo
# from mongoengine import connect

# from flask_mongoengine import MongoEngine
# db = MongoEngine(config=Config)

# connect to mongo db --shift this later
mongo = pymongo.MongoClient("mongodb+srv://dev:root@cluster0.x52x0kh.mongodb.net/?retryWrites=true&w=majority", connect=False)
db = mongo.get_database("shopping_db")

def create_app(config_class=Config):

    #Create flask application instance, __name__ var has the name of the current python module
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    # mongoengine
    # connect(host=app.config['MONGO_URI'])

    # pymongo
    # print(db.products)

    # Register blueprints here
    from webapp.auth import auth as auth
    app.register_blueprint(auth)

    from webapp.product_page import product_page as product
    app.register_blueprint(product)

    from webapp.order_page import order_page as order
    app.register_blueprint(order)

    # Initialise login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    from .models import User

    # Define user loader function
    @login_manager.user_loader
    def load_user(user_id):
        user = db.users.find_one({'_id': ObjectId(user_id)})
        print(user_id)
        if not user:
            return None
        return User(_id=user['_id'], username=user['username'], password=user['password'], role=user['role'], products=user['products'])

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# ap = create_app()
# login_manager.init_app(ap)

# from .models import User

# @login_manager.user_loader
# def load_user(username):
#     u = db.users.find_one({"username": username})
#     if not u:
#         return "No user"
#     return User(username=u["username"], password=u["password"], role=u["role"], products=u["products"])