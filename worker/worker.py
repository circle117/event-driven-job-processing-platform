import time
import random
import threading
from api.models.job import JobStatus


def process_job(job_id: str, jobs_db: dict):
    """
    mimic job processing
    """
    # update the status to processing
    jobs_db[job_id]["status"] = JobStatus.PROCESSING

    # mimic job processing
    time.sleep(random.uniform(2, 4))

    # mimic failure
    if random.random() < 0.3:
        jobs_db[job_id]["status"] = JobStatus.FAILED
        jobs_db[job_id]["error"] = "Random simulated failure"
        return
    
    # update the status to completed
    jobs_db[job_id]["status"] = JobStatus.COMPLETED


def run_worker_async(job_id: str, jobs_db: dict):
    """
    start a thread to run the job async
    """
    thread = threading.Thread(target=process_job, args=(job_id, jobs_db))
    thread.daemon = True
    thread.start()