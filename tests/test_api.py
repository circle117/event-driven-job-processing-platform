import requests
from constants import BASE_URL
from api.models.job import JobStatus

def test_create_job():
    response = requests.post(f"{BASE_URL}/jobs", json={
        "job_type": "test",
        "payload": {"key": "value"}
    })
    assert response.status_code == 201
    job = response.json()
    assert job["status"] == "pending"
    assert job["retry_count"] == 0
    assert "job_id" in job

def test_get_job():
    response = requests.post(f"{BASE_URL}/jobs", json={
        "job_type": "test",
        "payload": {"key": "value"}
    })
    assert response.status_code == 201
    job_id = response.json()["job_id"]

    # status should be pending or processing
    response = requests.get(f"{BASE_URL}/jobs/{job_id}")
    job = response.json()
    assert response.status_code == 200
    assert job["job_id"] == job_id
    assert job["status"] in (JobStatus.PENDING, JobStatus.PROCESSING)

def test_get_job_not_found():
    response = requests.get(f"{BASE_URL}/jobs/nonexistent-id")
    assert response.status_code == 404