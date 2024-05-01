#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib  # Add this import for hashing

class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if getenv("HBNB_TYPE_STORAGE") != "db":
            self.password = hashlib.md5(self.password.encode()).hexdigest()

    def save(self):
        """Hash the password before saving"""
        if getenv("HBNB_TYPE_STORAGE") != "db":
            self.password = hashlib.md5(self.password.encode()).hexdigest()
        super().save()

    def to_dict(self, include_password=False):  # Update this method
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = super().to_dict()
        if not include_password and "password" in new_dict:  # Exclude password
            del new_dict["password"]
        return new_dict

