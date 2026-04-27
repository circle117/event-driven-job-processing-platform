from fastapi.testclient import TestClient
import pytest
import requests
from unittest import mock

from api.models.job import JobStatus
from constants import BASE_URL, TEST_JOB_ID
from main import app

"""
Test that /jobs API calling works as expected
"""

client = TestClient(app)

@pytest.fixture
def mock_db():
    with mock.patch("services.database.table") as mock_db:
        yield mock_db

def test_create_job(mock_db):
    response = client.post(f"{BASE_URL}/jobs", json={
        "job_type": "test",
        "payload": {"key": "value"}
    })
    assert response.status_code == 201
    job = response.json()
    assert job["status"] == "pending"
    assert "job_id" in job
    mock_db.put_item.assert_called_once_with(
        Item = {
        "job_id": mock.ANY,
        "status": JobStatus.PENDING,
        "job_type": "test",
        "payload": {"key": "value"},
        "error": None,
        },
        ConditionExpression="attribute_not_exists(job_id)",
    )

def test_get_job(mock_db):
    response = client.get(f"{BASE_URL}/jobs/{TEST_JOB_ID}")
    mock_db.get_item.assert_called_once_with(Key={"job_id": TEST_JOB_ID})

def test_get_job_not_found(mock_db):
    mock_db.get_item.return_value = {}

    response = client.get(f"{BASE_URL}/jobs/nonexistent-id")
    assert response.status_code == 404