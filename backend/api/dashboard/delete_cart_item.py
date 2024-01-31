import json
from flask import jsonify, redirect, render_template, request, session, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from app.models import Login,db
from api.rolee_required import role_required


class del_cart_item(Resource):
        
    @jwt_required()
    @role_required('user')
    def delete(self,category_name,product_name,item_count):
        identity = get_jwt_identity()
        # print(category_name)
        # print(product_name)

        user = Login.query.filter_by(email=identity).first()
        
        cart_items_list = json.loads(user.cart_items)
        for i in cart_items_list:
            if i["product_name"] == product_name :
                print("deleting...")
                flag = False
                i['item_count'] -= item_count 
                    
                if(i['item_count'] == 0):
                    cart_items_list.remove(i)
                    
                user.cart_items = json.dumps(cart_items_list)
                break

        db.session.commit()
        
        # print(user.cart_items)
        # print(cart_item)
        
        
        return "success"
        
    


        

        
        

