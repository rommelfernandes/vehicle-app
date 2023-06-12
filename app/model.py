from util import S3Object
from config import s3_bucket, region

class Model:
    def __init__(self, backend_model = None):
        self.classifier = backend_model
        self.s3_client = S3Object(s3_bucket, region)

    def fit(self, feature_list):
        self.classifier.fit(feature_list)

    def save(self, model_file):
        self.s3_client.to_s3(self.classifier, model_file)

    def load(self, model_file):
        self.classifier = self.s3_client.from_s3(model_file)

    def predict(self, img):
        distances, indices = self.classifier.kneighbors(img)
        return distances, indices