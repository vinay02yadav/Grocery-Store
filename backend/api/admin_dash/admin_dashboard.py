from datetime import datetime,timedelta
from functools import wraps
from flask import jsonify, make_response, redirect, render_template, request, session, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, set_access_cookies
from flask_login import login_user
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from app.models import Category,Admin_Request,db,Product
from api.rolee_required import role_required

security_code = "secure_as_hell"


parser = reqparse.RequestParser()
parser.add_argument('name', type=str,help='Username is required !!')
parser.add_argument('new_name', type=str,help='Username is required !!')


class admin_dashboard(Resource):
    @jwt_required()
    @role_required('admin')
    def post(self):
        args = parser.parse_args()
        category_name = args.get('name')
        
        new_cat = Category(name=category_name.lower())
        db.session.add(new_cat)
        db.session.commit()
        self.delete(category_name.lower())
        
    @jwt_required()
    @role_required('admin')
    def put(self):
        args = parser.parse_args()
        category_name = args.get('name')
        new_name = args.get('new_name')
        
        new_cat = Category.query.filter_by(name=category_name).first()
        new_cat.name = new_name
        db.session.commit()
        self.delete((f'{new_name},{category_name}'))

        
    @jwt_required()
    @role_required('admin')
    def get(self):
        category = Admin_Request.query.all()
        cat_add_list=[]
        cat_edit_list=[]
        cat_delete_list=[]
        manager_list=[]
        
        for i in category:
            if(i.type == 'add_category'): 
                cat_add_list.append((i.category_name,i.manager_name))
            elif(i.type == 'edit_category'): 
                arr = i.category_name.split(',')
                cat_edit_list.append((arr[0],arr[1],i.manager_name))
            elif(i.type == 'delete_category'): 
                cat_delete_list.append((i.category_name,i.manager_name))
            else:
                manager_list.append((i.category_name,i.manager_name))
                
        return {'cat_add_list':cat_add_list,'cat_edit_list':cat_edit_list,'cat_delete_list':cat_delete_list,'manager_list':manager_list}
    
    
    @jwt_required()
    @role_required('admin')
    def delete(self,category):
        if('+' in category):
            cat = category.split('+')
            
            all_Category = Category.query.filter_by(name=cat[0]).first()
            
            cat_id = all_Category.id
            db.session.delete(all_Category)
            
            all_Products = Product.query.filter_by(category_id=cat_id).all()
            for i in all_Products:
                db.session.delete(i)
            
            
            user = Admin_Request.query.filter_by(category_name=cat[0]).first()
            db.session.delete(user)
                
            db.session.commit()
            
        else:
            user = Admin_Request.query.filter_by(category_name=category).first()
            db.session.delete(user)
            db.session.commit()

    
    
