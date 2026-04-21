import time
import random
import threading
from api.models.job import JobStatus


MAX_RETRIES = 3


def process_job(job_id: str, jobs_db: dict):
    """
    mimic job processing
    """
    # skip if it is in process or completed
    if jobs_db[job_id]["status"] in (JobStatus.PROCESSING, JobStatus.COMPLETED):
        return

    # update the status to processing
    jobs_db[job_id]["status"] = JobStatus.PROCESSING

    # mimic job processing
    time.sleep(random.uniform(2, 4))

    # mimic failure
    if random.random() < 0.3:
        retry_count = jobs_db[job_id]["retry_count"] + 1
        jobs_db[job_id]["retry_count"] = retry_count

        if retry_count < MAX_RETRIES:
            # set the status back to pending
            jobs_db[job_id]["status"] = JobStatus.PENDING
            jobs_db[job_id]["error"] = f"Failed, retrying ({retry_count}/{MAX_RETRIES})"
            
            # exponential backoff
            time.sleep(2**retry_count)
            process_job(job_id, jobs_db)
        else:
            jobs_db[job_id]["status"] = JobStatus.FAILED
            jobs_db[job_id]["error"] = f"Failed after {MAX_RETRIES} retries"
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