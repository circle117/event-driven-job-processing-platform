from fastapi import APIRouter, HTTPException
from api.models.job import JobStatus, JobCreate, JobResponse
from worker.worker import run_worker_async
import uuid


router = APIRouter()

# TODO: temporary storage, use DynamoDB later
jobs_db: dict = {}


@router.post("", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate):
    job_id = str(uuid.uuid4())
    job_data = {
        "job_id": job_id,
        "status": JobStatus.PENDING,
        "job_type": job.job_type,
        "payload": job.payload
    }
    jobs_db[job_id] = job_data

    run_worker_async(job_id, jobs_db)

    return job_data


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str):
    job = jobs_db.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job