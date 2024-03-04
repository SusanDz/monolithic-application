from flask_login import UserMixin
from webapp import db

class User(UserMixin):
    def __init__(self, _id, username, password, role, products):
        self._id = _id
        self.username = username
        self.password = password
        self.role = role
        self.products = products

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return str(self._id)
    
class Product():
    def __init__(self, _id, name, price, picture):
        self._id = _id
        self.name = name
        self.price = price
        self.picture = picture
