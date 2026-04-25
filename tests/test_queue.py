import pytest
from unittest import mock
from services.queue import send_job, receive_jobs, delete_job_message, WAIT_TIME_SECONDS

from conftest import TEST_JOB_ID
    
def test_send_job(mock_sqs):
    send_job(TEST_JOB_ID)
    mock_sqs.send_message.assert_called_once_with(
        QueueUrl=mock.ANY,
        MessageBody=TEST_JOB_ID,
    )

def test_receive_jobs(mock_sqs):
    mock_sqs.receive_message.return_value = {
        "Messages": [
            {"MessageId": "1", "Body": TEST_JOB_ID, "ReceiptHandle": "handle-1"},
            {"MessageId": "2", "Body": "other-job", "ReceiptHandle": "handle-2"},
        ]
    }

    messages = receive_jobs()
    assert len(messages) == 2
    assert messages[0]["Body"] == TEST_JOB_ID
    mock_sqs.receive_message.assert_called_once_with(
        QueueUrl=mock.ANY,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=WAIT_TIME_SECONDS,
    )

def test_receive_jobs_empty(mock_sqs):
    mock_sqs.receive_message.return_value = {}
    messages = receive_jobs()
    assert messages == []

def test_delete_job_message(mock_sqs):
    delete_job_message("receipt-handle-123")
    mock_sqs.delete_message.assert_called_once_with(
        QueueUrl=mock.ANY,
        ReceiptHandle="receipt-handle-123",
    )