from flask import send_file
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required

from flask import current_app as app
from app.tasks import *

# -------------- 

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True,
                    help='Username is required !!')

class ExportAPI(Resource):
    @jwt_required()
    def get(self): 
        with app.app_context():
            print("satrting")
            task = export_csv.delay()

            result = task.wait()
            print(result)
            # print(task)

            csv_path = result['csv_path']
            response = send_file(csv_path, as_attachment=True)

            return response
        
class getting_img(Resource):
    @jwt_required()
    def post(self): 
        args = parser.parse_args()
        name = args.get('name')
        print(name)
        
        with app.app_context():
            print("collecting")
            # task = gett_img.delay(name)
            gett_img.delay(name)

            # result = task.wait()
            # print(result)
            # print(task)

            print("Image collected")
