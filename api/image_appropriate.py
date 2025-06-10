from PIL import Image
from transformers.pipelines import pipeline

classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")



def get_image_appropriateness(image_path: str) -> int:
    '''
    Classify the appropriateness of an image using a pretrained NSFW model.
    Args:
        image_path (str): Path to the image file.
    Returns:
        float: Appropriateness score (0-1), where 0 is inappropriate and 1 is appropriate.
    '''
    img = Image.open(image_path)
    classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
    result = classifier(img)
    top_score = max(result, key=lambda x: x['score']) # type: ignore #Should be valid
    if top_score['label'] == 'nsfw':
        return 1 - top_score['score']
    return top_score['score']