from setfit import SetFitModel
from huggingface_hub import login, logout
from dotenv import load_dotenv
import os

load_dotenv()

token = os.environ["HF_TOKEN"]
login(token)
model = SetFitModel.from_pretrained("FriedGil/rockd-image-relevance-classification")


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