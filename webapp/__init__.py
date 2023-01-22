from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

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

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app