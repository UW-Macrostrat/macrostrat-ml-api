import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv
import os

load_dotenv()


# bucket_name = "ml-model-data"
# prefix = "rockd-text-relevance-model/"
# local_dir = "./rockd-text-relevance-model-download"

base_url = "https://storage.macrostrat.org"
access_key = os.environ["MODELS_S3_ACCESS_KEY"]
secret_key = os.environ["MODELS_S3_SECRET_KEY"]

s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=base_url,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

def download_model_from_folder(bucket, prefix, local_dir):
    try:
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            if "Contents" not in page:
                print("No objects found with that prefix.")
                return
            for obj in page["Contents"]:
                key = obj["Key"]
                rel_path = os.path.relpath(key, prefix)
                local_file_path = os.path.join(local_dir, rel_path)

                if key.endswith("/"):  #Ensure folder exists
                    os.makedirs(local_file_path, exist_ok=True)
                    continue

                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                print(f"Downloading s3://{bucket}/{key} to {local_file_path}")
                s3.download_file(bucket, key, local_file_path)
    except Exception as e:
        print(f"Error downloading model from folder: {e}")

def download_model_from_file(bucket, key, local_file_path):
    try:
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        print(f"Downloading s3://{bucket}/{key} to {local_file_path}")
        s3.download_file(bucket, key, local_file_path)
    except Exception as e:
        print(f"Error downloading model from file: {e}")