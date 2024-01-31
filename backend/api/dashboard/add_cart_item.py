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

# def role_required(role):
#     user = Login.query.filter_by(email=get_jwt_identity()).first()
#     if user.role == role:
#         return True
#     else:
#         return False
    




class cart_item(Resource):
    @jwt_required()
    @role_required('user')
    def post(self):
        # if(role_required('user')):
        identity = get_jwt_identity()
        args = parser.parse_args()
        product_name =  args.get('product_name')
        category_name =  args.get('category_name')
        item_count =  args.get('item_count')

        user = Login.query.filter_by(email=identity).first()
        
        # result1 = Category.query.filter_by(name=category_name).first()
        result = Product.query.filter_by(name=product_name).first()

        print(result)
        
        cart_item = {
            'product_name': product_name,
            'category_name': category_name,
            'item_count': item_count,
            'rate': result.rate,
            'quantity': result.quantity,
            'unit': result.unit,
            'stock': result.stock,
            'image_link': result.image_link,
        }
        flag = True
        
        if user.cart_items == "":
            user.cart_items = json.dumps([cart_item])
        else:
            cart_items_list = json.loads(user.cart_items)
            for i in cart_items_list:
                if i["product_name"] == product_name:
                    flag = False
                    i['item_count'] = item_count 
                    user.cart_items = json.dumps(cart_items_list)
                    break

            if flag:
                cart_items_list.append(cart_item)
                user.cart_items = json.dumps(cart_items_list)

        db.session.commit()
        
        # print(user.cart_items)
        # print(cart_item)
        
        
        return "success"
    
        # else:
        #     return 'forbidden'
        
        
        
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()

        user = Login.query.filter_by(email=identity).first()
        try:
            arr = json.loads(user.cart_items)
            
            for i in arr:
                details = Product.query.filter_by(name=i['product_name']).first()
                i['stock'] = details.stock
                i['rate'] = details.rate
                i['quantity'] = details.quantity
            
            user.cart_items = json.dumps(arr)
                
            if(arr == []):
                return {'message':arr,'user':identity, 'data':'empty'}
            else:
                return {'message':arr,'user':identity, 'data':'non-empty'}
            
        except json.decoder.JSONDecodeError as e:
            return {'message':'','user':identity}
        
  

        
