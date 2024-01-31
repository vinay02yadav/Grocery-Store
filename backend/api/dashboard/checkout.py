import json
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from app.models import Login, db, Product
import datetime
from api.rolee_required import role_required

dic={}

class checkout(Resource):

    @jwt_required()
    @role_required('user')
    def get(self):
        identity = get_jwt_identity()
        # print(category_name)
        # print(product_name)

        user = Login.query.filter_by(email=identity).first()

        cart_items_list = json.loads(user.cart_items)
        
        flag = False
        
        if user.previous_order:
            previous_orders = json.loads(user.previous_order)
            flag = True
            
        
        for i in cart_items_list:
            product = Product.query.filter_by(name=i["product_name"]).first()
            if(product in dic.keys()):
                dic[product] += product.quantity * i["item_count"]
            else:
                dic[product] = product.quantity * i["item_count"]
                
            product.stock -= product.quantity * i["item_count"]
            
            current_datetime = datetime.datetime.now()

            i['time'] = current_datetime.strftime("%d %B %Y %H:%M:%S")

            if(flag):
                previous_orders.append(i)
            
            # if(len(previous_orders) != 0):
            # previous_orders.append(previous_item)
            
         
            
        if(not flag):
            previous_orders = cart_items_list
                
        user.previous_order = json.dumps(previous_orders)
        print(previous_orders)
        print(user.previous_order)
        
        cart_items_list.clear()
        user.cart_items = json.dumps(cart_items_list)

        db.session.commit()

        return "success"
