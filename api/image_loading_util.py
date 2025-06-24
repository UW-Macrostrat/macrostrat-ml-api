import requests
from PIL import Image
from io import BytesIO

def get_image_from_id(checkin_id: int, person_id: int):
    """
    Retrieve an image based on the person ID and image ID.
    """
    url = f"https://dev.rockd.org/api/protected/image/{person_id}/thumb_large/{checkin_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except requests.RequestException as e:
        print(f"Error fetching image: {e}")
        return Image.new('RGB', (100, 100), color='white')
    except IOError as e:
        print(f"Error opening image: {e}")
        return Image.new('RGB', (100, 100), color='white')  # Return a blank image on error
