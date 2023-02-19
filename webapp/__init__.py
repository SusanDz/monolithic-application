from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class=Config):

    #Create flask application instance, __name__ var has the name of the current python module
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    db = SQLAlchemy()
    db.init_app(app)

    # Register blueprints here
    from webapp.auth import auth as auth
    app.register_blueprint(auth)

    from webapp.product_page import product_page as product
    app.register_blueprint(product)

    from webapp.order_page import order_page as order
    app.register_blueprint(order)

    # from .models import User

    # with app.app_context():
    #     db.create_all()

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
# from os import path
# def create_database(app):
#     if not path.exists('webapp/mono.db'):
#         db.create_all(app=app)
#         print('Created Database!')