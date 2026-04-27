import boto3
from config import AWS_REGION, SQS_QUEUE_URL

WAIT_TIME_SECONDS = 5

sqs = boto3.client("sqs", region_name=AWS_REGION)

def send_job(job_id: str):
    sqs.send_message(
        QueueUrl = SQS_QUEUE_URL,
        MessageBody = job_id,
    )

def receive_jobs(max_messages: int = 10) -> list:
    response = sqs.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages = max_messages,
        WaitTimeSeconds=WAIT_TIME_SECONDS,
        AttributeNames=["ApproximateReceiveCount"],
    )
    return response.get("Messages", [])

def delete_job_message(receipt_handle: str):
    sqs.delete_message(
        QueueUrl=SQS_QUEUE_URL,
        ReceiptHandle=receipt_handle,
    )

def change_message_visibility(receipt_handle: str, timeout: int):
    sqs.change_message_visibility(
        QueueUrl=SQS_QUEUE_URL,
        ReceiptHandle=receipt_handle,
        VisibilityTimeout=timeout,
    )
