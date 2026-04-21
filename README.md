# Job Platform on AWS
This is an event-driven job processing platform for AWS practice.

## Tech Stack

Programming Language: Python 3.11

Backend Framework: FastAPI

Cloud Services: AWS (SQS, DynamoDB, S3, CloudWatch, Lambda/EC2)

## Plan

Phase 1: Local implementation

- [ ] Backend implementation with FastAPI
  - [x] `POST /jobs`
  - [x] `GET /jobs/{job_id}`
- [x] Worker implementation
  - [x] One simple worker function
  - [x] Job status change (pending -> processing -> completed/failed)
  - [x] Async execution
- [ ] Error handling and idempotency
  - [ ] No repetitive execution for same job_id
  - [ ] Error handling
  - [ ] Retry

Phase 2: basic AWS services

- [ ] DynamoDB
  - [ ] Create tables
  - [ ] Replace in-memory storage with DynamoDB
- [ ] SQS
- [ ] DLQ + Retry

Phase 3: Observability + S3

- [ ] CloudWatch Logs + structured logs
- [ ] CloudWatch Metrics + Alarms
- [ ] S3

Phase 4: Deployment (Lambda or EC2)

- [ ] Deployment
- [ ] IAM Permissions
- [ ] Test
