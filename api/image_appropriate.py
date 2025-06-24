from PIL import Image
from transformers.pipelines import pipeline

from image_loading_util import get_image_from_id


classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")



def get_image_appropriateness(checkin_id: int, person_id: int) -> float:
    '''
    Classify the appropriateness of an image using a pretrained NSFW model.
    Args:
        image_path (str): Path to the image file.
    Returns:
        float: Appropriateness score (0-1), where 0 is inappropriate and 1 is appropriate.
    '''
    image = get_image_from_id(checkin_id, person_id)
    classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
    result = classifier(image)
    top_score = max(result, key=lambda x: x['score']) # type: ignore #Should be valid
    if top_score['label'] == 'nsfw':
        return 1 - top_score['score']
    return top_score['score']