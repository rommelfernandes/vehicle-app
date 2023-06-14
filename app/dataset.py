
from io import BytesIO
import base64

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, ResNet50
import numpy as np
from numpy.linalg import norm
from PIL import Image

from util import S3Object
from config import (s3_bucket, 
                    region,
                    images_folder
)


class Dataset:
    def __init__(self):
        self.s3_client = S3Object(s3_bucket, region)
        self.transfer_model = ResNet50(weights='imagenet', include_top=False,
                 input_shape=(224, 224, 3))
        self.filenames = sorted(self.s3_client.list_objects(Prefix = images_folder))
        self.feature_list  = [self.extract_features(self.extract_image_s3(file), self.transfer_model) for file in self.filenames[1:]]


    def extract_image_s3(self, img_path):
        """
        extracts images from s3 bucket and resizes it

        Args:
            img_path: location of image on s3 within a bucket 
            (ex. 'images/test.jpg')
        
        Returns:
            image file
        
        """
        input_shape = (224, 224, 3)
        img = self.s3_client.from_s3(img_path).resize(
            size =(input_shape[0], input_shape[1])
            )
        return img

    @classmethod
    def extract_features(cls, img, transfer_model):
        """
        Extracts features based on Resnet50 trained model for new and existing
        images

        Args:
            img: image file
            transfer_model: TensorFlow model used for transfer learning
        
        Returns:
            Array with normalized features from transformation
        """
        img_array = image.img_to_array(img)
        expanded_img_array = np.expand_dims(img_array, axis=0)
        preprocessed_img = preprocess_input(expanded_img_array)
        features = transfer_model.predict(preprocessed_img)
        flattened_features = features.flatten()
        normalized_features = flattened_features / norm(flattened_features)
        return normalized_features

    @staticmethod
    def moments(image):
        """
        Static helper function that takes a image file and finds its moments

        Args: 
            image: image file 

        Returns:
            mu_vector, covariance_vector
        """

        c0, c1 = np.mgrid[:image.shape[0], :image.shape[1]]
        img_sum = np.sum(image)
        
        m0 = np.sum(c0 * image) / img_sum
        m1 = np.sum(c1 * image) / img_sum
        m00 = np.sum((c0-m0)**2 * image) / img_sum
        m11 = np.sum((c1-m1)**2 * image) / img_sum
        m01 = np.sum((c0-m0) * (c1-m1) * image) / img_sum
        
        mu_vector = np.array([m0,m1])
        covariance_matrix = np.array([[m00, m01],[m01, m11]])
        
        return mu_vector, covariance_matrix

    @staticmethod
    def deskew(image):
        """
        Static Helper function for skewing images 

        Args:
            image: image file 
        
        Returns:
            transformed image file
        """
        c, v = moments(image)
        alpha = v[0,1] / v[0,0]
        affine = np.array([[1,0], [alpha,1]])
        ocenter = np.array(image.shape) / 2.0
        offset = c - np.dot(affine, ocenter)

        return interpolation.affine_transform(image, affine, offset=offset)

    @staticmethod
    def get_np_image(image_bytes):
        """
        Static helper function that transforms image byes to np array

        Args:
            image_bytes: byte converted image data
        
        Return:
            Numpy array of images
        """

        image = Image.open(BytesIO(base64.b64decode(image_bytes))).convert(mode='L')
        image = image.resize((28, 28))

        return np.array(image)