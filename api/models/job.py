from pydantic import BaseModel
from enum import Enum


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobCreate(BaseModel):
    """Job request data"""
    job_type: str
    payload: dict = {}


class JobResponse(BaseModel):
    """job response data"""
    job_id: str
    status: JobStatus
    job_type: str
    payload: dict
    error: str | None = None