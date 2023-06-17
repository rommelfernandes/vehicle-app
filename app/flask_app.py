import sys
import os
from flask import Flask, send_file, request, jsonify
from PIL import Image
from flask_restful import Api, Resource
import logging

sys.path.append(os.getcwd())
from predict import output
from util import S3Object
from config import s3_bucket, region,images_folder

app = Flask(__name__)
api = Api(app)

class Predict(Resource):

    def post(self):
        file = request.files['image']
        # Read the image via file.stream
        img = Image.open(file.stream).resize(
            size =(224, 224)
            )
        
        file1, file2 = output(img)
        return jsonify({'msg': 'success', 
                        'file1': file1,
                        'file2': file2,
                        })
    
class Addfile(Resource):
    
    def post(self):
        file = request.files['image']
        img= Image.open(file.stream)
        file_name = img['image'].name.split('/')[-1]
        s3_client = S3Object(s3_bucket, region)
        s3_client.to_s3(img, images_folder + file_name)
        return jsonify({'msg': 'success',
                         'file': f'file {file_name} added to S3'
                         })


api.add_resource(Predict, '/predict')
api.add_resource(Addfile, '/add')

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    app.run(debug=True, host='0.0.0.0', port=5000) # change debug=False in production
    logging.info('App finished')