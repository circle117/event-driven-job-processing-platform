# Job Platform on AWS
This is an event-driven job processing platform for AWS practice.

## Tech Stack

Programming Language: Python 3.11

Backend Framework: FastAPI

Cloud Services: AWS (SQS, DynamoDB, S3, CloudWatch, Lambda/EC2)

## Plan

Phase 1: Local implementation

- [x] Backend implementation with FastAPI
  - [x] `POST /jobs`
  - [x] `GET /jobs/{job_id}`
- [x] Worker implementation
  - [x] One simple worker function
  - [x] Job status change (pending -> processing -> completed/failed)
  - [x] Async execution
- [x] Error handling and idempotency
  - [x] No repetitive execution for same job_id
  - [x] Error handling
  - [x] Retry

Phase 2: basic AWS services

- [x] DynamoDB
  - [x] Create tables
  - [x] Replace in-memory storage with DynamoDB
- [x] SQS
  - [x] Add SQS
- [x] DLQ + Retry
  - [x] Let SQS handle retry
  - [x] Exponential backoff

Phase 3: Observability + S3

- [x] CloudWatch Logs + structured logs
  - [x] Structured logging
  - [x] CloudWatch Logs
- [ ] CloudWatch Metrics + Alarms
- [ ] S3

Phase 4: Deployment (Lambda or EC2)

- [ ] Deployment
- [ ] IAM Permissions
- [ ] Test

## Note

To ensure idempotency, the SQS Visibility timeout must be longer than the maximum job processing time. If processing time is unpredictable or unbounded, conditional writes and a timestamp should be used instead.
