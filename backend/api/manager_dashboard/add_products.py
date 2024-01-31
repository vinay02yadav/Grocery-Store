from datetime import datetime,timedelta
from functools import wraps
from flask import jsonify, make_response, redirect, render_template, request, session, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import login_user
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from app.models import Product,Category,Admin_Request,db
from api.rolee_required import role_required

security_code = "secure_as_hell"

parser = reqparse.RequestParser()
parser.add_argument('category_name', type=str, required=True,help='Username is required !!')
parser.add_argument('original_product_name', type=str,help='Username is required !!')
parser.add_argument('product_name', type=str, required=True,help='Username is required !!')
parser.add_argument('rate', type=str, required=True,help='Username is required !!')
parser.add_argument('quantity', type=str, required=True,help='Username is required !!')
parser.add_argument('unit', type=str, required=True,help='Username is required !!')
parser.add_argument('stock', type=str, required=True,help='Username is required !!')
parser.add_argument('expiry', type=str, required=True,help='Username is required !!')


class products(Resource):
    @jwt_required()
    @role_required(['manager', 'admin'])
    def post(self):
        print("post..........................")
        args = parser.parse_args()
        category_name = args.get('category_name')
        product_name = args.get('product_name')
        rate = args.get('rate')
        quantity = args.get('quantity')
        expiry = args.get('expiry')
        unit = args.get('unit')
        stock = args.get('stock')
        
        category_id = Category.query.filter_by(name=category_name).first().id

        user = Product.query.filter_by(category_id=category_id,name=product_name).first()

        if user == None: 
            product = Product(category_id=category_id,name=product_name,rate=rate,quantity=quantity,unit=unit,stock=stock,expiry=expiry,image_link="")
            db.session.add(product)
            db.session.commit()
            return 'success'
        else:
            return 'unsuccess'
        
    @jwt_required()
    @role_required(['manager', 'admin'])
    def get(self,category_name):
        category = Category.query.filter_by(name=category_name).first()
        products = Product.query.filter_by(category_id=category.id).all()
        
        # name expiry rate quantity unit stock
        dic=[]
        for i in products:
            dic.append({'name':i.name,
                        'expiry':i.expiry,
                        'rate':i.rate,
                        'quantity':i.quantity,
                        'unit':i.unit,
                        'stock':i.stock,
                        })
            
        # print(dic)

        return jsonify({'status': 'success','list' : dic})
    
    @jwt_required()
    @role_required(['manager', 'admin'])
    def delete(self,category_name,product_name):
        category = Category.query.filter_by(name=category_name).first()
        products = Product.query.filter_by(category_id=category.id,name=product_name).first()
        print(products)
        
        db.session.delete(products)
        db.session.commit()

        return 'success'
    
    @jwt_required()
    @role_required(['manager', 'admin'])
    def put(self):
        args = parser.parse_args()
        category_name = args.get('category_name')
        original_product_name = args.get('original_product_name')
        product_name = args.get('product_name')
        rate = args.get('rate')
        quantity = args.get('quantity')
        unit = args.get('unit')
        stock = args.get('stock')
        expiry = args.get('expiry')
        
        category_id = Category.query.filter_by(name=category_name).first().id
        
        product = Product.query.filter_by(category_id=category_id,name=original_product_name).first()
        
        product.name = product_name
        product.rate = rate
        product.quantity = quantity
        product.unit = unit
        product.stock = stock
        product.expiry = expiry
        
        db.session.commit()

        return 'success'

    
    
