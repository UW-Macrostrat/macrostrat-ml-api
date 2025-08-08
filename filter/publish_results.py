import os
import requests
from models import Report

def publish_feedback(report: Report):
    if report is None:
        raise ValueError("Cannot publish feedback: report is None")
    
    url = "https://dev.rockd.org/api/protected/checkins-feedback"
    token = os.getenv("INTEGRATION_TOKEN_SECRET")
    if not token:
        raise ValueError("INTEGRATION_TOKEN_SECRET environment variable is not set")

    headers = {
        "authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=report.to_dict(), headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Failed to publish feedback: {response.status_code} - {response.text}")
    else:
        print(f"Successfully published feedback: {response.status_code} - {response.text}")
