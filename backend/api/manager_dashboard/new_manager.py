from datetime import datetime,timedelta
from functools import wraps
from flask import flash, jsonify, make_response, redirect, render_template, request, session, url_for,current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import login_user
from flask_restful import Resource, abort, reqparse
from werkzeug.security import generate_password_hash
from app.models import Login,Admin_Request,db
from itsdangerous import URLSafeTimedSerializer

import smtplib
import ssl
from email.message import EmailMessage

app = current_app
app.config['SECRET_KEY'] = "secure_as_hell"
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

security_code = "secure_as_hell"


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True,help='Username is required !!')
parser.add_argument('password', type=str, required=True,help='Username is required !!')

dic={}

def send_email(email):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('726ryadav@gmail.com', 'bjtzpedlxrimemlt')
        
        token = serializer.dumps(email, salt='email-confirm')
        confirm_url = url_for('confirm_email', token=token, _external=True)

        em = EmailMessage()
        em['From'] = '726ryadav@gmail.com'
        em['To'] = email
        em['Subject'] = "Register on Urahara's Shop"
        em.set_content(f"Click the following link to confirm your email: {confirm_url}")

        server.send_message(em)

        print("Email sent successfully.")
        return True
    
    except Exception as e:
        print(e)
        return False

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
        print(f'Email confirmed: {email}')     
        print(dic.get('password'))   
        
        ad_user = Admin_Request.query.filter_by(type='manager',manager_name=dic.get('email')).first()
        if(ad_user == None):
            new_cat = Admin_Request(category_name=f"{generate_password_hash(dic.get('password'))}", type='manager',manager_name=dic.get('email'))
            db.session.add(new_cat)
            db.session.commit()
                
        flash('Verified.\nGoto Login Page', 'success')
        
        return render_template('confirm_mail.html',message="Request has been sent to admin.  Please wait...")
    
    except Exception as e:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return abort(204)





class new_manager(Resource):
    def post(self):
        args = parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        
        dic['password'] = password
        dic['email'] = username
        
        print(dic.get('password'))
        print(dic.get('email'))
        
        user = Login.query.filter_by(email=username).first()
        ad_user = Admin_Request.query.filter_by(type='manager',manager_name=username).first()
        print(ad_user)
        
        if user == None and ad_user == None:
            if send_email(username):
                return {'status': 'confirm_link_send'}
            else:
                return {'status': 'no such email'}
            
        elif(ad_user != None):
            return 'already present'
        else:
            return 'unsuccess'
        

    
    
