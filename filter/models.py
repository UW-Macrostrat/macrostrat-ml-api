from typing import Optional
from pydantic import BaseModel

class Checkin(BaseModel):
    photo_id: Optional[int]  # Allow None
    person_id: int
    checkin_id: int
    notes: str

class Report(BaseModel):
    checkin_id: int
    photo_id: Optional[int]
    text_relevancy: float
    image_relevancy: float
    text_appropriateness: float
    image_appropriateness: float
    status_code: int

    def to_dict(self):
        return self.dict()
