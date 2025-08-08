import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO

load_dotenv()

def get_image_from_id(photo_id: int, person_id: int):

    token = os.getenv("INTEGRATION_TOKEN_SECRET")
    if not token:
        raise ValueError("INTEGRATION_TOKEN_SECRET environment variable is not set")
    headers = {
        "authorization": f"Bearer {token}"
    }

    """
    Retrieve an image based on the person ID and image ID.
    """
    url = f"https://rockd.org/api/protected/image/{person_id}/thumb_large/{photo_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except requests.RequestException as e:
        print(f"Error fetching image: {e}")
        return Image.new('RGB', (100, 100), color='white')
    except IOError as e:
        print(f"Error opening image: {e}")
        return Image.new('RGB', (100, 100), color='white')  # Return a blank image on error
