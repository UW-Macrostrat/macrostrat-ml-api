from api.schemas import Checkin
from fastapi import FastAPI
from api.text_relevance import get_relevance_score
from api.text_appropriate import get_text_appropriateness
from api.image_appropriate import get_image_appropriateness

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
    relevance_score = get_relevance_score(checkin.notes)
    approp_text_score = get_text_appropriateness(checkin.notes)

    image_appropriateness = checkin.photo is not None  # Placeholder for image appropriateness che
    return {"checkin_id": checkin.checkin_id, 
            "relevance_score": relevance_score,
            "text_appropriateness": approp_text_score,
            }

# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8000)
