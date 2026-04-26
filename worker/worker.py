import random
import time
from api.models.job import JobStatus
from services import database, queue

MAX_RETRIES = 3

def process_job(job_id: str):
    """
    mimic job processing
    """
    job = database.get_job(job_id)

    # skip if it is in process or completed
    if job["status"] == JobStatus.COMPLETED:
        return

    # update the status to processing
    database.update_job(job_id, {"status": JobStatus.PROCESSING})

    # mimic job processing
    time.sleep(random.uniform(2, 4))

    # mimic failure
    if random.random() < 0.3:
        database.update_job(job_id, {"status": JobStatus.FAILED,
                                     "error": "Random failure"})
        raise Exception("Random failure")
    
    # update the status to completed
    database.update_job(job_id, {
        "status": JobStatus.COMPLETED
    })


def run_worker():
    while True:
        messages = queue.receive_jobs()
        for message in messages:
            job_id = message["Body"]
            receipt_handle = message["ReceiptHandle"]
            try:
                print(f"Processing job: {job_id}")
                process_job(job_id)
                queue.delete_job_message(receipt_handle)
            except Exception as e:
                print(f"Error processing job {job_id}: {e}")