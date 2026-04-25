import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

from config import AWS_REGION

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table("jobs")

def create_job(job_data: dict):
    table.put_item(Item=job_data)

def get_job(job_id: str) -> dict | None:
    response = table.get_item(Key={"job_id": job_id})
    item = response.get("Item")
    if item:
        return _deserialize(item)
    return None

def update_job(job_id: str, updates: dict):
    expressions = []
    values = {}
    names = {}

    for key, value in updates.items():
        placeholder = f"#attr_{key}"
        expressions.append(f"{placeholder} = :{key}")
        values[f":{key}"] = value
        names[placeholder] = key
    
    table.update_item(
        Key = {"job_id": job_id},
        UpdateExpression="SET " + ", ".join(expressions),
        ExpressionAttributeValues=values,
        ExpressionAttributeNames=names,
    )

def delete_job(job_id: str):
    """
    delete job in database, only used for testing
    """
    table.delete_item(Key={"job_id": job_id})

def _deserialize(job: dict) -> dict:
    return {
        k: int(v) if isinstance(v, Decimal) else v
        for k, v in job.items()
    }