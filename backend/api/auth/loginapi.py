from datetime import datetime,timedelta
from functools import wraps
from flask import jsonify, make_response, redirect, render_template, request, session, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, set_access_cookies
from flask_login import login_user
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from app.models import Login,db

security_code = "secure_as_hell"


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True,
                    help='Username is required !!')
parser.add_argument('password', type=str, required=True,
                    help='Password is required !!')


class loginapi(Resource):
    
    def set_cookie(self,access_token):
        res = make_response("cookie set sucess")
        res.set_cookie("access_token", access_token,samesite='None',httponly=True)
        # res.set_cookie("heyy", "yoyo",samesite='None',httponly=True)
        # print(request.cookies.get("access_token"))
        # session['access_token'] = access_token
        return res
    
    def get_coo(self):
        print(session.get('access_token'))
                

    def post(self):
        args = parser.parse_args()
        username = args.get('username')
        password = args.get('password')

        user = Login.query.filter_by(email=username).first()
        print(user)
        
        if(user):
            print(user)
            if user.email == username and  check_password_hash(user.password,password):
                print(user)
                
                user.timestamp = datetime.now()
                db.session.commit()
                
                refresh_token = create_refresh_token(identity=username, expires_delta=timedelta(seconds=20))
                access_token = create_access_token(identity=username, expires_delta=timedelta(hours=24))
                
                return jsonify({'status': 'success','message': 'Successfully logged in !!', 'access_token': access_token, 'refresh_token': refresh_token , "username": username,'role':user.role,'id':user.id})

            else:
                print("else")
                return jsonify({'status': 'unsuccessful'})
            
        else:
            print("else")
            return jsonify({'status': 'unsuccessful'})
        
    
    def get(self):
        print("getting......")
        access_token = request.cookies.get("access_token")
        # access_token = session.get('access_token')
        print(access_token)
        return jsonify({'status': 'success','message': 'Successfully logged in !!', 'access_token': access_token})

    
    

class RefreshTokenAPI(Resource):
    @jwt_required(refresh=True)
    def post(self):
        # access_token = request.cookies.get("access_token")
        # print(access_token)
        # access_token = session.get('access_token')
        # print(access_token)
        
        
        print("inside refresh ")
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, expires_delta=timedelta(seconds=10))
        return {'access_token': access_token}, 200