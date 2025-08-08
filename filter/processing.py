from models import Checkin, Report
from image_relevance import get_image_relevance_score
from text_relevance import get_relevance_score
from text_appropriate import get_text_appropriateness
from image_appropriate import get_image_appropriateness

def generate_checkin_report(checkin: Checkin) -> Report:
    print(f"Processing checkin: {checkin.photo_id} for person {checkin.person_id}")
    
    text_relevance_score = get_relevance_score(checkin.notes)
    text_appropriateness_score = get_text_appropriateness(checkin.notes)

    if checkin.photo_id is None:
        image_relevance_score = 1.0
        image_appropriateness_score = 1.0
    else:
        image_relevance_score = get_image_relevance_score(checkin.photo_id, checkin.person_id)
        image_appropriateness_score = get_image_appropriateness(checkin.photo_id, checkin.person_id)

    # Determine status code
    status_code = 1
    if text_relevance_score < 0.5:
        status_code = 10
    elif image_relevance_score < 0.5:
        status_code = 11
    elif text_appropriateness_score < 0.5:
        status_code = 12
    elif image_appropriateness_score < 0.5:
        status_code = 13

    return Report(
        checkin_id=checkin.checkin_id,
        photo_id=checkin.photo_id,
        text_relevancy=text_relevance_score,
        image_relevancy=image_relevance_score,
        text_appropriateness=text_appropriateness_score,
        image_appropriateness=image_appropriateness_score,
        status_code=status_code
    )
