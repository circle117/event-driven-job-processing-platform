import sys
import os

import pytest
from unittest import mock

from api.models.job import JobStatus
from services.database import create_job, delete_job

sys.path.insert(0, os.path.dirname(__file__))

BASE_URL = "http://localhost:8000"
TEST_JOB_ID = "test-job-123"

@pytest.fixture(autouse=True)
def setup_job():
    create_job({
        "job_id": TEST_JOB_ID,
        "status": JobStatus.PENDING,
        "job_type": "test",
        "payload": {"key": "value"},
        "retry_count": 0,
        "error": None,
    })
    yield
    delete_job(TEST_JOB_ID)

@pytest.fixture
def no_sleep():
    with mock.patch("worker.worker.time.sleep"):
        yield

@pytest.fixture
def mock_sqs():
    with mock.patch("services.queue.sqs") as mock_sqs:
        yield mock_sqs