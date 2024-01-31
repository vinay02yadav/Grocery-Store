import json
from flask import jsonify, redirect, render_template, request, session, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from app.models import Login,db,Category,Product
from api.rolee_required import role_required

parser = reqparse.RequestParser()
parser.add_argument('product_name', type=str, required=True, help='id is required')
parser.add_argument('category_name', type=str, required=True, help='id is required')
parser.add_argument('item_count', type=int, required=True, help='id is required')

class cart_item(Resource): 
        
    @jwt_required()
    @role_required('user')
    def get(self):
        identity = get_jwt_identity()

        user = Login.query.filter_by(email=identity).first()
        try:
            arr = json.loads(user.cart_items)
            if(arr == []):
                return {'message':arr,'user':identity, 'data':'empty'}
            else:
                return {'message':arr,'user':identity, 'data':'non-empty'}
            
        except json.decoder.JSONDecodeError as e:
            return {'message':'','user':identity}
        
  

        

        
        

