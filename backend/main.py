from datetime import datetime, timedelta
from celery import Celery
from flask import Flask, config, flash, redirect, render_template, request, session, url_for
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
import matplotlib
from flask_session import Session

matplotlib.use('Agg')
import os
from functools import wraps
from flask import Flask, request, jsonify, make_response
from app.models import db

import app.workers as workers
from app.tasks import *

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

app = Flask(__name__)
app.config.from_object(config)
app.app_context().push()

from api.auth.loginapi import loginapi,RefreshTokenAPI
from api.auth.register import registerapi

from api.dashboard.dashboard import dashboard
from api.dashboard.add_cart_item import cart_item
from api.dashboard.delete_cart_item import del_cart_item
from api.dashboard.checkout import checkout

from api.manager_dashboard.manager_dash import store_manager_dashboard
from api.manager_dashboard.new_manager import new_manager
from api.manager_dashboard.add_products import products

from api.admin_dash.admin_dashboard import admin_dashboard
from api.admin_dash.add_manager import add_manager_from_admin
from api.export.exportAPI import ExportAPI,getting_img

from get_images import get_img 
from get_images import * 




cors = CORS(app,supports_credentials=True)  

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response

basedir = os.path.abspath(os.path.dirname(__file__))

basedir = (basedir.replace("\\","/")) 

app.config['SQLALCHEMY_BINDS'] = {"db1":'sqlite:///' +basedir+'/databases/login_credentials.sqlite3',
                                  "db2":'sqlite:///' +basedir+'/databases/catogories.sqlite3',
                                  "db3":'sqlite:///' +basedir+'/databases/products.sqlite3',
                                  "db4":'sqlite:///' +basedir+'/databases/admin_requests.sqlite3',}
db.init_app(app)

app.config['SECRET_KEY'] = 'secure_as_hell'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

api = Api(app)
api.init_app(app)

JWTManager(app)



# CELERY -----------

celery = workers.celery

celery.conf.update(
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    timezone = 'Asia/Calcutta',
    enable_utc = False
)

celery.Task = workers.ContextTask
app.app_context().push()


api.add_resource(loginapi, '/api/login')
api.add_resource(registerapi, '/api/register')
api.add_resource(RefreshTokenAPI, '/api/token/refresh')

api.add_resource(dashboard, '/dashboard')
api.add_resource(cart_item, '/add_cart_item')
api.add_resource(del_cart_item, '/delete_cart_item/<string:category_name>/<string:product_name>/<int:item_count>')
api.add_resource(checkout, '/checkout')

api.add_resource(store_manager_dashboard, '/store_manager_dashboard')
api.add_resource(new_manager, '/new_manager')

api.add_resource(admin_dashboard, '/admin_dashboard', '/admin_dashboard/<string:category>')
api.add_resource(add_manager_from_admin, '/add_manager_from_admin','/add_manager_from_admin/<string:username>/<string:password>')

api.add_resource(products, '/products','/<string:category_name>/products','/<string:category_name>/<string:product_name>/products')
api.add_resource(ExportAPI, '/api/export-posts-csv')

api.add_resource(getting_img, '/get-img')
api.add_resource(get_img, '/get_img/<string:product_name>')


if __name__ == '__main__':
    app.run(debug=True)
    get_img.get()




# start redis-server

# run main.py file

# cd backend
# celery -A main.celery worker --pool=solo -l info



# open in another terminal
# cd backend
# celery -A main.celery beat --max-interval 600 -l info


# cd frontend
# npm run serve