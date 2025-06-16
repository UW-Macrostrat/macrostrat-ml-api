from transformers.pipelines import pipeline
from image_loading_util import get_image_from_id

checkpoint = "openai/clip-vit-base-patch32"
detector = pipeline(model=checkpoint, task="zero-shot-image-classification")

def get_image_relevance_score(image_id: int) -> float:
    """
    Get the relevance score for a given image and text using a zero-shot image classification model.
    Args:
        image_id (int): The ID of the image.
        text (str): The text to evaluate against the image.
    Returns:
        float: The relevance score between 0 and 1. 1 is high relevance, 0 is low relevance.
    """
    image = get_image_from_id(image_id).convert('RGB')
    predictions = detector(image, candidate_labels=["strata", "misc"])
    return predictions[0]['score'] if predictions[0]['label'] == "strata" else 1 - predictions[0]['score'] # type: ignore