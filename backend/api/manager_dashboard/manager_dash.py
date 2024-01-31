from datetime import datetime, timedelta
from functools import wraps
from flask import jsonify, make_response, redirect, render_template, request, session, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import login_user
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from app.models import Category, Admin_Request, db
from api.rolee_required import role_required

security_code = "secure_as_hell"


parser = reqparse.RequestParser()
parser.add_argument('category', type=str, required=True,
                    help='Username is required !!')
parser.add_argument('category_type', type=str,
                    help='Username is required !!')
parser.add_argument('original_category', type=str,
                    help='Username is required !!')


class store_manager_dashboard(Resource):
    @jwt_required()
    @role_required(['manager', 'admin'])
    def post(self):
        args = parser.parse_args()
        category_name = args.get('category').lower()
        category_type = args.get('category_type')
        original_category = args.get('original_category')

        print(category_name, category_type)

        if (category_type == 'Add'):

            user = Category.query.filter_by(name=category_name).first()

            if user == None:
                new_cat = Admin_Request(
                    category_name=category_name, type='add_category', manager_name=get_jwt_identity())
                db.session.add(new_cat)
                db.session.commit()
                return 'success'
            else:
                return 'unsuccess'

        elif (category_type == 'Edit'):

            user = Category.query.filter_by(name=original_category).first()
            print(original_category)

            if user != None:
                new_cat = Admin_Request(category_name=(
                    f'{category_name},{original_category}'), type='edit_category', manager_name=get_jwt_identity())
                db.session.add(new_cat)
                db.session.commit()
                return 'success'
            else:
                return 'unsuccess'

    @jwt_required()
    @role_required(['admin', 'manager'])
    def get(self):
        category = Category.query.all()
        dic = {}
        for i in category:
            dic[i.id] = i.name

        return jsonify({'status': 'success', 'list': dic, 'identity': get_jwt_identity()})


    @jwt_required()
    @role_required(['manager', 'admin'])
    def put(self):
        args = parser.parse_args()
        category = args.get('category')
        
        user = Admin_Request.query.filter_by(category_name=category,type='delete_category').first()
        
        if user == None:
            new_cat = Admin_Request(category_name=category, type='delete_category', manager_name=get_jwt_identity())
            db.session.add(new_cat)
            db.session.commit()
            return 'success'
        else:
            return 'unsuccess'
