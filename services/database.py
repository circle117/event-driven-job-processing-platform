import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("jobs")

def create_job(job_data: dict):
    table.put_item(Item=job_data)

def get_job(job_id: str) -> dict | None:
    response = table.get_item(Key={"job_id": job_id})
    return response.get("Item")

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