
from flask import Flask, send_file, request, jsonify
from PIL import Image
from flask_restful import Api, Resource
import logging

from predict import output

app = Flask(__name__)
api = Api(app)

class Predict(Resource):
    def post(self):
        file = request.files['image']
        # Read the image via file.stream
        img = Image.open(file.stream).resize(
            size =(224, 224)
            )
        
        img1, img2 = output(img)
        return jsonify({'msg': 'success', 
                        'size': [img.width, img.height],
                        'size1': [img1.width, img1.height],
                        'size2': [img2.width, img2.height],
                        })



api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    app.run(debug=True, host='0.0.0.0', port=5000) # change debug=False in production
    logging.info('App finished')