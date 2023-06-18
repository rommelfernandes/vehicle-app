from sklearn.neighbors import NearestNeighbors

from dataset import Dataset
from model import Model

# using abstraction to hide unnecessary code and only present what
# data scientists would use to update the model (get data, get features, choose model
# train model, save model)

# Get Data
image_dataset = Dataset()

# Generate Features
feature_list = image_dataset.feature_list
filenames = image_dataset.filenames

# backend_Model
backend_model = NearestNeighbors(n_neighbors=3, algorithm="brute", metric="euclidean")

# Modeling
model = Model(backend_model=backend_model)
model.fit(feature_list)

# Save Models and data
model.save("models/toy-vehicles-resnet-knn.pkl")
image_dataset.s3_client.to_s3(image_dataset.transfer_model, "models/resnet50.pkl")
image_dataset.s3_client.to_s3(feature_list, "data/feature_list.pkl")
image_dataset.s3_client.to_s3(filenames, "data/filenames.pkl")
print("complete")
