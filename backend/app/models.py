from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()

class Login(UserMixin,db.Model):
    __bind_key__ = 'db1'
    __tablename__ = 'login'
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    email = db.Column(db.String, unique=True,nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String)
    cart_items = db.Column(db.String)
    previous_order = db.Column(db.String)
    
class Category(UserMixin,db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key=True,autoincrement = True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)

    
class Product(UserMixin,db.Model):
    __bind_key__ = 'db3'
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key=True,autoincrement = True, nullable=False)
    name = db.Column(db.String, nullable=False)
    expiry = db.Column(db.String, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String)
    

class Admin_Request(UserMixin,db.Model):
    __bind_key__ = 'db4'
    __tablename__ = 'requests'
    category_name = db.Column(db.String,primary_key=True, nullable=False)
    manager_name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

