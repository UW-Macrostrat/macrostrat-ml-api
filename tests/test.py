import requests


def get_unchecked():
    """Fetch items that need processing from external API"""
    resp = requests.get("https://dev.rockd.org/api/protected/checkins?needs_screening=true")
    data = resp.json()
    return data["success"]["data"]

print(get_unchecked())


