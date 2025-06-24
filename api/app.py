from schemas import Checkin
from fastapi import FastAPI
from image_relevance import get_image_relevance_score
from text_relevance import get_relevance_score
from text_appropriate import get_text_appropriateness
from image_appropriate import get_image_appropriateness
import uvicorn

app = FastAPI(title="RockD Data Screening API")

@app.get("/")
def index():
    return "Use /checkin to process checkin data."


@app.post("/checkin")
def get_checkin_report(checkin: Checkin):
    """
    Process a checkin and return a relevance score.
    
    Args:
        checkin (Checkin): The checkin data containing ID and notes.
        
    Returns:
        dict: A dictionary containing the checkin ID and its relevance score.
    """
    text_relevance_score = get_relevance_score(checkin.notes)
    image_relevance_score = get_image_relevance_score(checkin.checkin_id, checkin.person_id)
    text_appropriateness_score = get_text_appropriateness(checkin.notes)
    image_appropriateness_score = get_image_appropriateness(checkin.checkin_id, checkin.person_id)

    return {"checkin_id": checkin.checkin_id, 
            "text_relevanve": text_relevance_score,
            "image_relevance": image_relevance_score,
            "text_appropriateness": text_appropriateness_score,
            "image_appropriateness": image_appropriateness_score,
            }

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
