import pytest
import requests
import time

from constants import BASE_URL
from api.models.job import JobStatus

@pytest.mark.skip()
def test_job_lifecycle():
    response = requests.post(f"{BASE_URL}/jobs", json={
        "job_type": "test",
        "payload": {"key": "value"}
    })

    assert response.status_code == 201
    job = response.json()
    job_id = job["job_id"]
    assert job["status"] == JobStatus.PENDING

    final_status = None
    for _ in range(15):
        time.sleep(2)
        response = requests.get(f"{BASE_URL}/jobs/{job_id}")
        job = response.json()
        print(f"status: {job['status']}, retry_count: {job['retry_count']}")
        if job["status"] in (JobStatus.COMPLETED, JobStatus.FAILED):
            final_status = job["status"]
            break
    
    assert final_status in ("completed", "failed"), "Job did not complete in time"

@pytest.mark.skip()
def test_multiple_jobs():
    """
    post multiple jobs
    """
    job_ids = []

    for i in range(5):
        response = requests.post(f"{BASE_URL}/jobs", json={
            "job_type": "test",
            "payload": {"index": i}
        })
        assert response.status_code == 201
        job_ids.append(response.json()["job_id"])
    
    for _ in range(30):
        time.sleep(2)
        statuses = []
        for job_id in job_ids:
            job = requests.get(f"{BASE_URL}/jobs/{job_id}").json()
            statuses.append(job["status"])

        print(f"statuses: {statuses}")
        if all(s in ("completed", "failed") for s in statuses):
            break

    assert all(s in ("completed", "failed") for s in statuses), \
        f"Some jobs did not complete: {statuses}"