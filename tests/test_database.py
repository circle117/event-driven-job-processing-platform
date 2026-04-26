import botocore
import pytest

from api.models.job import JobStatus
from constants import TEST_JOB_ID
from services.database import get_job, update_job, create_job


def test_create_and_get_job():
    job = get_job(TEST_JOB_ID)
    assert job is not None
    assert job["job_id"] == TEST_JOB_ID
    assert job["status"] == JobStatus.PENDING
    assert job["retry_count"] == 0

def test_create_one_job_twice():
    with pytest.raises(botocore.exceptions.ClientError) as exc_info:
        create_job({
            "job_id": TEST_JOB_ID,
            "status": JobStatus.PENDING,
            "job_type": "test",
            "payload": {"key1": "value"},
            "retry_count": 0,
            "error": None,
        })
    assert exc_info.value.response["Error"]["Code"] == "ConditionalCheckFailedException"

def test_get_nonexistent_job():
    job = get_job("nonexistent-id")
    assert job is None

def test_update_job_status():
    update_job(TEST_JOB_ID, {"status": JobStatus.PROCESSING})
    job = get_job(TEST_JOB_ID)
    assert job["status"] == JobStatus.PROCESSING

def test_update_job_retry_count():
    update_job(TEST_JOB_ID, {"retry_count": 2})
    job = get_job(TEST_JOB_ID)
    assert job["retry_count"] == 2

def test_update_job_error():
    update_job(TEST_JOB_ID, {"error": "something went wrong"})
    job = get_job(TEST_JOB_ID)
    assert job["error"] == "something went wrong"

def test_update_multiple_fields():
    update_job(TEST_JOB_ID, {
        "status": JobStatus.FAILED,
        "retry_count": 3,
        "error": "Failed after 3 retries",
    })
    job = get_job(TEST_JOB_ID)
    assert job["status"] == JobStatus.FAILED
    assert job["retry_count"] == 3
    assert job["error"] == "Failed after 3 retries"