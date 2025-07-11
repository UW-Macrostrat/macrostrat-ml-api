from rq.job import Job
from schemas import Checkin
from image_relevance import get_image_relevance_score
from text_relevance import get_relevance_score
from text_appropriate import get_text_appropriateness
from image_appropriate import get_image_appropriateness
from redis import Redis
import requests

redis_conn = Redis()

def generate_checkin_report(checkin: Checkin):
    print(f"Processing checkin: {checkin.photo_id} for person {checkin.person_id}")
    """
    Generate a relevance and appropriateness report for a checkin.
    """
    try:
        text_relevance_score = get_relevance_score(checkin.notes)
        image_relevance_score = get_image_relevance_score(checkin.photo_id, checkin.person_id)
        text_appropriateness_score = get_text_appropriateness(checkin.notes)
        image_appropriateness_score = get_image_appropriateness(checkin.photo_id, checkin.person_id)
        #Threshold is 0.5 for each. 9 is good, 10 is flagged for text relevance, 11 for image relevance, 12 for text appropriateness, and 13 for image appropriateness.
        status_code = 9
        if text_relevance_score < 0.5:
            status_code = 10
        elif image_relevance_score < 0.5:
            status_code = 11
        elif text_appropriateness_score < 0.5:
            status_code = 12
        elif image_appropriateness_score < 0.5:
            status_code = 13
        result = {
            "checkin_id": checkin.checkin_id,
            "photo_id": checkin.photo_id, 
            "text_relevancy": text_relevance_score,
            "image_relevancy": image_relevance_score,
            "text_appropriateness": text_appropriateness_score,
            "image_appropriateness": image_appropriateness_score,
            "status_code": status_code
        }
        return result

    except Exception as e:
        print(f"Failed to process checkin: {e}")
        return None

def publish_feedback(report_job_id: str):
    job = Job.fetch(report_job_id, connection=redis_conn)
    job.refresh()  # In case job has just finished
    report: Checkin = job.result
    #Append to File (or create if it doesnt exist)
    if report is None:
        raise ValueError(f"Report job {report_job_id} has no result yet.")
    #make a post request to /protected/checkins/feedback with report as body:
    response = requests.post(
        "http://rockd.org/api/protected/checkins/feedback",
        json=report
    )
    if response.status_code != 200:
        raise ValueError(f"Failed to publish feedback: {response.status_code} - {response.text}")
    else:
        print(f"Successfully published feedback: {response.status_code} - {response.text}")