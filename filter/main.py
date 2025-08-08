import time
from dotenv import load_dotenv

from api import get_unchecked, parse_checkin
from processing import generate_checkin_report
from publish_results import publish_feedback

load_dotenv()



def process_checkins():
    """Poll API every 10s and process new checkins synchronously"""
    while True:
        try:
            unchecked = get_unchecked()
            for item in unchecked:
                checkin = parse_checkin(item)
                report = generate_checkin_report(checkin)
                publish_feedback(report)
                print(f"Processed: {checkin}")
        except Exception as e:
            print(f"Error while polling: {e}")
        time.sleep(10)

if __name__ == "__main__":
    process_checkins()
