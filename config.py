from dotenv import load_dotenv
import os

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
LOG_GROUP = os.getenv("LOG_GROUP", "/job-platform")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")