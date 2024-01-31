from flask import jsonify, redirect, render_template, request, session, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from app.models import Product,Category,Login

from flask_caching import Cache
from flask import current_app as app
cache = Cache(app)


class dashboard(Resource):
    @jwt_required()
    def post(self):
        pass
    
    @cache.cached(timeout=150)
    def get(self):
        print("inside dashboard get")
        # print(get_jwt_identity())
        product = Product.query.all()
        category = Category.query.all()
        
        cat = {}
        for i in category:
            cat[i.id] = i.name
        
        check_id=[]
        result = {}
        
        for i in product:
            if(i.category_id in check_id):
                result[cat[i.category_id]].append({
                        'name': i.name,
                        'rate': i.rate,
                        'quantity': i.quantity,
                        'unit': i.unit,
                        'image_link': i.image_link,
                        'stock': i.stock,
                    })
            else:
                result[ cat[i.category_id] ] = [
                    {
                        'name': i.name,
                        'rate': i.rate,
                        'quantity': i.quantity,
                        'unit': i.unit,
                        'image_link': i.image_link,
                        'stock': i.stock,
                    }
                ]
                check_id.append(i.category_id)
                
        # print(result)
                
        return {'message':'success','products':result}

        

        
        

