from setfit import SetFitModel
import os

from model_loading_util import download_model_from_folder


try:
    model = SetFitModel.from_pretrained("FriedGil/rockd-image-relevance-classification")

except Exception as e:
    download_model_from_folder("ml-model-data", "rockd-text-relevance-model/", "./rockd-text-relevance-model-download")
    model = SetFitModel.from_pretrained("./rockd-text-relevance-model-download")




def get_relevance_score(text: str) -> float:
    """
    Get the relevance score for a given text.
    
    Args:
        text (str): The input text to evaluate.
        
    Returns:
        float: The relevance score between 0 and 1. 1 is high relevance, 0 is low relevance.
    """
    # Use the model to predict the relevance score
    score = float(model.predict_proba([text])[0][0])
    return score