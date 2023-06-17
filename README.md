## Vehicle Similarity App

#### Description
My two year old son has an affinity for hotwheels and cars in general. This is an image similarity app that uses ResNet50 as a transfer learning model and Nearest Neighbors to identify similar cars when we go out and buy new ones.

#### Language and Technologies
Existing collection of hotwheels images are loaded and saved to and S3 bucket. Feature extraction is then performed using the ResNet50 model architecture and TensorFlow. The extracted features are then loaded into a Nearest Neighbors model, where K similar images are presented when a new image is uploaded. The backend of this model is ran using TensorFlow, scikit-Learn, and served using Flask Restful API. The API is deployed using Docker containers and AWS services (ECS, ECR, and Fargate, and S3). A web app will be generated for user access.  


#### Future Features

* Intialize training when new images are added using UI
* Add feature to capture hotwheels image and find potential value.
