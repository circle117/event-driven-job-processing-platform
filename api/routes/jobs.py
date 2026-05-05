from fastapi import APIRouter, HTTPException
from logger import get_logger
import uuid

from api.models.job import JobStatus, JobCreate, JobResponse
from services import database, queue


router = APIRouter()
logger = get_logger(__name__, "api")

@router.post("", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate):
    job_id = str(uuid.uuid4())
    job_data = {
        "job_id": job_id,
        "status": JobStatus.PENDING,
        "job_type": job.job_type,
        "payload": job.payload,
        "error": None,
    }
    database.create_job(job_data)
    logger.info("Job created", extra={"job_id": job_id, "job_type": job.job_type})
    queue.send_job(job_id)
    
    return job_data

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str):
    job = database.get_job(job_id)
    if not job:
        logger.warning("Job not found", extra={"job_id": job_id})
        raise HTTPException(status_code=404, detail="Job not found")
    return job