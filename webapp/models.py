from flask_login import UserMixin
from flask_pymongo import PyMongo

mongo = PyMongo()

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, TypeVar, Annotated
from bson.objectid import ObjectId as BsonObjectId

T = TypeVar('T')  # or a bound=SupportGt

ObjectIdStr = List[Annotated[T, BsonObjectId]]

class User(BaseModel, UserMixin):
    _id: Optional[ObjectIdStr] = None
    username: str = Field(min_length=4)
    password: str = Field(min_length=8) # regex
    role: Optional[str] = None # Literal
    products: Optional[ObjectIdStr[BsonObjectId]] = []

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # def __init__(self, _id, username, password, role, products):
    #     self._id = _id
    #     self.username = username
    #     self.password = password
    #     self.role = role
    #     self.products = products

    #     username = mongo.db.StringField()
    #     password = db.StringField()
    #     mail = db.StringField()

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
    
    # def to_json(self):
    #     return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data
    
class Product():
    def __init__(self, _id, name, price, picture):
        self._id = _id
        self.name = name
        self.price = price
        self.picture = picture
