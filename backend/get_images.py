# from app.models import Product,db
# from flask_restful import Resource, reqparse

# from google_images_search import GoogleImagesSearch

# def fetch_images(query):
#     gis = GoogleImagesSearch('AIzaSyCqErUvIqbCgNbAWCzOFvMSNmjWtesKxXo', '57beb9fbbd81e4c46')

#     search_params = {
#         'q': query,
#         'num': 1,
#         'safe': 'off',
#     }

#     try:
#         gis.search(search_params=search_params)
#         image_urls = [result.url for result in gis.results()]

#         return image_urls

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
    
    
# class get_img(Resource):
#     def get():
#         products = Product.query.filter_by().all()
        
#         for product in products:
#             print(product.name,product.image_link)
#             if(product.image_link == None or product.image_link == ""):
#                 product.image_link = fetch_images(product.name)[0]
            
#         db.session.commit()
        
#         print("Ready to Go..")

# # print(fetch_images("meat"))

import os
import requests
from app.models import Product, db
from flask_restful import Resource

basedir = os.path.abspath(os.path.dirname(__file__))

basedir = (basedir.replace("\\","/")) 
basedir = basedir[:-7] + "frontend/public/images"

    
from bing_image_downloader import downloader
    
def download_images(query):
    r = downloader.download(query, limit=1,  output_dir=basedir,adult_filter_off=True, force_replace=False, timeout=20)
    print(r)




class get_img(Resource):
    def get():
        products = Product.query.filter_by().all()

        for product in products:
            print(product.name, product.image_link)
            if product.image_link is None or product.image_link == "":
                download_images(product.name)
                files = os.listdir(basedir + f"/{product.name}")
                product.image_link = f'images/{product.name}/{files[0]}'

        db.session.commit()

        print("Ready to Go..")
    



