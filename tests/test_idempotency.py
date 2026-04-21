import requests
import time

BASE_URL = "http://localhost:8000"

response = requests.post(f"{BASE_URL}/jobs", json={
    "job_type": "test",
    "payload": {"key": "value"}
})
job = response.json()
job_id = job["job_id"]
print(f" Created job: {job_id}, status: {job['status']}")

for i in range(8):
    time.sleep(1)
    response = requests.get(f"{BASE_URL}/jobs/{job_id}")
    job = response.json()
    print(f"{i+1} sec - status: {job['status']}, retry_count: {job['retry_count']}, error: {job.get('error')}")