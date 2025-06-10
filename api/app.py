from schemas import Checkin
import uvicorn
from fastapi import FastAPI

from text_relevance import get_relevance_score

app = FastAPI(title="RockD Data Screening API")

@app.post("/checkin")
def get_checkin_report(checkin: Checkin):
    """
    Process a checkin and return a relevance score.
    
    Args:
        checkin (Checkin): The checkin data containing ID and notes.
        
    Returns:
        dict: A dictionary containing the checkin ID and its relevance score.
    """
    score = get_relevance_score(checkin.notes)
    return {"checkin_id": checkin.checkin_id, "relevance_score": score}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
