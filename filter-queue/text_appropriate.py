from transformers.pipelines import pipeline

# Load a pretrained toxicity classifier model from Hugging Face
classifier = pipeline("text-classification", model="unitary/toxic-bert", tokenizer="unitary/toxic-bert")

def get_text_appropriateness(text: str) -> int:
    '''
    Classify the appropriateness of a text caption using a pretrained model.
    Args:
        text (str): Text to classify.
    Returns:
        float: Appropriateness score (0-1), where 0 is inappropriate and 1 is appropriate.
    '''
    result = classifier(text)
    score = 1 - result[0]['score'] # type: ignore
    return score # type: ignore
