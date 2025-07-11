from pydantic import BaseModel

class Checkin(BaseModel):
    photo_id: int
    person_id: int
    checkin_id: int
    notes: str