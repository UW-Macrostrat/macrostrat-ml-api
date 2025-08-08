import requests
from models import Checkin

def get_unchecked():
    """Fetch items that need processing from external API"""
    resp = requests.get("https://dev.rockd.org/api/protected/checkins?needs_screening=true")
    data = resp.json()
    return data["success"]["data"]

def parse_checkin(item) -> Checkin:
    return Checkin(
        photo_id=int(item["photo"]) if item["photo"] is not None else None,
        person_id=int(item["person_id"]),
        checkin_id=int(item["checkin_id"]),
        notes=item["notes"]
    )
