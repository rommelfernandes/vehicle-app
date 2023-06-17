import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


s3_bucket = os.environ.get("s3_bucket")
region = os.environ.get("region")
data_folder = os.environ.get("data_folder")
images_folder = os.environ.get("images_folder")
model_folder = os.environ.get("model_folder")
