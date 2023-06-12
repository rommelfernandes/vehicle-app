from model import Model
from util import S3Object
from dataset import Dataset
from config import s3_bucket, region

def output(img):
    """
    Takes in image and outputs two similar images based on images 
    in repository

    Args:
        img: image file

    Returns:
        two similar images based on model 
    """
    s3_client = S3Object(s3_bucket, region)
    filenames = s3_client.from_s3('data/filenames.pkl')
    transfer_model =  s3_client.from_s3('models/resnet50.pkl')
    model = Model()
    model.load('models/toy-vehicles-resnet-knn.pkl')
    img = Dataset.extract_features(img, transfer_model)
    distances, indices=model.predict(img)
    img1 = s3_client.from_s3(filenames[indices[0][1]])
    img2 = s3_client.from_s3(filenames[indices[0][2]])
    return img1, img2

