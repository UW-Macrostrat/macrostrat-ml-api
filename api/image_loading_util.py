from PIL import Image
import os
import io
from dotenv import load_dotenv
import boto3
from botocore.client import Config

load_dotenv()

base_url = "https://storage.macrostrat.org"
access_key = os.environ["PHOTOS_S3_ACCESS_KEY"]
secret_key = os.environ["PHOTOS_S3_SECRET_KEY"]

def get_image_from_id(image_id: int) -> Image.Image:
    """
    Get the image URL from the image ID. 
    This has to search through the entire S3 bucket to find the image, so ideally this can be changed.
    
    Args:
        image_id (str): The ID of the image.
        
    Returns:
        Image: A PIL Image object of the image.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=base_url,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

    bucket_name = "rockd-photos"
    key = f"original/{image_id}.jpg"

    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        image_data = response['Body'].read()
        return Image.open(io.BytesIO(image_data))
    except Exception as e:
        print(f"Error retrieving image {image_id}: {e}")
        return None