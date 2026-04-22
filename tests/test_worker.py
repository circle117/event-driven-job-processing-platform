from unittest.mock import patch, MagicMock

from api.models.job import JobStatus
from conftest import BASE_URL, TEST_JOB_ID
from services.database import get_job, update_job
from worker.worker import process_job, MAX_RETRIES

def test_idempotency(no_sleep):
    """
    test that multiple workers get the job
    but only one actually works on it
    """
    with patch("worker.worker.random.random", return_value=0.99), \
        patch("services.database.update_job", wraps=update_job) as mock_update:
        process_job(TEST_JOB_ID)            # worker 1
        process_job(TEST_JOB_ID)            # worker 2
    
    # called twice, one for processing, another for completed
    assert mock_update.call_count == 2

def test_retry(no_sleep):
    # process failed
    with patch("worker.worker.random.random", return_value=0):
        process_job(TEST_JOB_ID)
    
    job = get_job(TEST_JOB_ID)
    assert job["retry_count"] == MAX_RETRIES
    assert job["status"] == JobStatus.FAILED
    assert job["error"] == f"Failed after {MAX_RETRIES} retries"
    