import random
import time
from api.models.job import JobStatus
from logger import get_logger
from services import database, queue

MAX_RETRIES = 3
logger = get_logger(__name__)

def process_job(job_id: str):
    """
    mimic job processing
    """
    job = database.get_job(job_id)

    # skip if it is in process or completed
    if job["status"] == JobStatus.COMPLETED:
        logger.info("Job already completed, skipping", extra={"job_id": job_id})
        return

    # update the status to processing
    database.update_job(job_id, {"status": JobStatus.PROCESSING})
    logger.info("Job started", extra={"job_id": job_id})

    # mimic job processing
    time.sleep(random.uniform(2, 4))

    # mimic failure
    if random.random() < 0.3:
        database.update_job(job_id, {"status": JobStatus.FAILED,
                                     "error": "Random failure"})
        logger.error("Job failed", extra={"job_id": job_id, "error": "Random failure"})
        raise Exception("Random failure")
    
    # update the status to completed
    database.update_job(job_id, {
        "status": JobStatus.COMPLETED
    })
    logger.info("Job completed", extra={"job_id": job_id})


def run_worker():
    logger.info("Worker started, polling SQS...")
    while True:
        messages = queue.receive_jobs()
        for message in messages:
            job_id = message["Body"]
            receipt_handle = message["ReceiptHandle"]
            receive_count = int(message["Attributes"]["ApproximateReceiveCount"])
            try:
                process_job(job_id)
                queue.delete_job_message(receipt_handle)
            except Exception as e:
                logger.error("Job failed",
                             extra={"job_id": job_id, "receive_count": receive_count, "error": str(e)})
                backoff = min(2**receive_count, 300)
                queue.change_message_visibility(receipt_handle, backoff)