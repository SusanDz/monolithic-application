# import os

# basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'Final dissertation 2023'

    # establish connection with sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mono.db'