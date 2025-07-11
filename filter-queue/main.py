import asyncio
import redis
import requests
from rq import Queue
from rq.worker import SimpleWorker
from schemas import Checkin
from tasks import publish_feedback, generate_checkin_report

# Connect to Redis
redis_conn = redis.Redis()
q = Queue('default', connection=redis_conn)

def get_unchecked():
    """Fetch items that need processing from external API"""
    resp = requests.get("https://dev.rockd.org/api/protected/checkins?needs_screening=true")
    data = resp.json()
    return data["success"]["data"]

async def poll_and_enqueue():
    """Poll API every 60s and enqueue new jobs"""
    while True:
        try:
            unchecked = get_unchecked()
            for item in unchecked:
                checkin = Checkin(
                    photo_id=item["photo"],
                    person_id=item["person_id"],
                    checkin_id=item["checkin_id"],
                    notes=item["notes"]
                )

                # Enqueue report generation
                report_job = q.enqueue(generate_checkin_report, checkin)

                # Enqueue feedback publishing
                q.enqueue(publish_feedback, report_job.id, depends_on=report_job)

                print(f"Enqueued: {checkin}")
        except Exception as e:
            print(f"Error while polling: {e}")
        await asyncio.sleep(60)

async def run_worker():
    """Run an RQ worker in burst mode every second"""
    # Empty the queue at startup (optional)
    q.empty()
    print("Queue emptied before starting the worker.")

    worker = SimpleWorker(queues=[q], connection=redis_conn)

    while True:
        # Process all available jobs, then return
        worker.work(burst=True)
        await asyncio.sleep(1)  # Wait a bit before checking again

async def main():
    # Run both loops concurrently
    await asyncio.gather(
        run_worker(),
        poll_and_enqueue()
    )

if __name__ == "__main__":
    asyncio.run(main())
