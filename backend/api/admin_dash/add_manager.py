from datetime import datetime,timedelta
from functools import wraps
from flask import jsonify, make_response, redirect, render_template, request, session, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, set_access_cookies
from flask_login import login_user
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from app.models import Login,Admin_Request,db
from api.rolee_required import role_required

security_code = "secure_as_hell"


parser = reqparse.RequestParser()
parser.add_argument('username', type=str,help='Username is required !!')
parser.add_argument('password', type=str,help='Username is required !!')


class add_manager_from_admin(Resource):
    @jwt_required()
    @role_required('admin')
    def post(self):
        args = parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        
        new_man = Login(email=username,password=password,role='manager',cart_items="")
        db.session.add(new_man)
        db.session.commit()
        self.delete(username,password)
    
    
    @jwt_required()
    @role_required('admin')
    def delete(self,username,password):
        user = Admin_Request.query.filter_by(category_name=password,manager_name=username).first()
        db.session.delete(user)
        db.session.commit()

    
    
