from typing import Optional
from pydantic import BaseModel

class Checkin(BaseModel):
    checkin_id: int
    notes: str
    person_id: Optional[int] = None
    rating: Optional[int] = None
    st_astext: Optional[str] = None
    photo: Optional[int] = None
    flagged: Optional[bool] = None
    status: Optional[str] = None
    likes: Optional[int] = None