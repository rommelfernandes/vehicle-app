import os
import pickle
from io import BytesIO, StringIO

import boto3
import pandas as pd
from PIL import Image


class S3ObjectInvalidExtension(Exception):
    pass


class S3ObjectUploadFailed(Exception):
    pass


class S3Object(object):
    def __init__(self, bucket, region_name):
        self.s3 = boto3.client("s3", region_name=region_name)
        self.bucket = bucket

    def list_objects(self, Prefix=None):
        """
        list items in S3 bucket by prefix Folder

        Args:
            Prefix: folder names within the bucket (ex. images/)
        """
        response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=Prefix)
        content = [content["Key"] for content in response.get("Contents", [])]
        return content

    def from_s3(self, key):
        """
        This method can  read csv, img files, and pickle files
        from S3 bucket

        Args:
            key: file name directory (ex. 'images/test.csv')
        """
        file_byte_string = self.s3.get_object(Bucket=self.bucket, Key=key)[
            "Body"
        ].read()
        ext = self.get_extension(key)
        if ext in ["PKL", "PICKLE", "PCK", "PCL"]:
            return pickle.loads(file_byte_string)
        elif ext in ["CSV"]:
            return pd.read_csv(BytesIO(file_byte_string))
        elif ext in ["JPG", "JPEG", "PNG"]:
            print(key)
            return Image.open(BytesIO(file_byte_string))

    def to_s3(self, obj, key):
        """
        Pushes data to S3 bucket either images, csv , or pickle files

        Args:
            obj: object to send to s3
            key: file name directory (ex. 'images/test.csv')
        """
        ext = self.get_extension(key)
        if ext in ["JPG", "JPEG", "PNG"]:
            buffer = BytesIO()
            obj.save(buffer, self.get_safe_ext(key))
            buffer.seek(0)
        elif ext in ["CSV"]:
            print("test")
            buffer = StringIO()
            obj.to_csv(buffer, index=False)
            buffer = buffer.getvalue()
        elif ext in ["PKL", "PICKLE", "PCK", "PCL"]:
            buffer = pickle.dumps(obj)
        sent_data = self.s3.put_object(Bucket=self.bucket, Key=key, Body=buffer)
        # sent_data = self.s3.upload_file(Bucket=self.bucket, Key=key, ) )
        if sent_data["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise S3ObjectUploadFailed(
                "Failed to upload image {} to bucket {}".format(key, self.bucket)
            )

    def delete_object(self, key):
        """
        Deletes object in S3 bucket

        Args:
            key: file name directory (ex. 'images/test.csv')
        """
        self.s3.delete_object(Bucket=self.bucket, Key=key)

    @staticmethod
    def get_extension(key):
        return os.path.splitext(key)[-1].strip(".").upper()

    @staticmethod
    def get_safe_ext(key):
        ext = os.path.splitext(key)[-1].strip(".").upper()
        if ext in ["JPG", "JPEG"]:
            return "JPEG"
        elif ext in ["PNG"]:
            return "PNG"
        else:
            raise S3ObjectInvalidExtension("Extension is invalid")
