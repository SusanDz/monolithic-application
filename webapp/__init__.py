from flask import Flask

from config import Config

def create_app(config_class=Config):

    #Create flask application instance, __name__ var has the name of the current python module
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app