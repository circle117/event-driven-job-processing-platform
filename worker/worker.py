import random
import time
import threading
from api.models.job import JobStatus
from services import database, queue

MAX_RETRIES = 3

def process_job(job_id: str):
    """
    mimic job processing
    """
    job = database.get_job(job_id)

    # skip if it is in process or completed
    if job["status"] in (JobStatus.PROCESSING, JobStatus.COMPLETED):
        return

    # update the status to processing
    database.update_job(job_id, {"status": JobStatus.PROCESSING})

    # mimic job processing
    time.sleep(random.uniform(2, 4))

    # mimic failure
    if random.random() < 0.3:
        retry_count = job["retry_count"] + 1

        if retry_count < MAX_RETRIES:
            # set the status back to pending
            database.update_job(job_id, {
                "status": JobStatus.PENDING,
                "retry_count": retry_count,
                "error": f"Failed, retrying ({retry_count}/{MAX_RETRIES})",
            })
            queue.send_job(job_id)
        else:
            database.update_job(job_id, {
                "status": JobStatus.FAILED,
                "retry_count": retry_count,
                "error": f"Failed after {MAX_RETRIES} retries",
            })
        return
    
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
            print(f"Processing job: {job_id}")
            process_job(job_id)
            queue.delete_job_message(receipt_handle)