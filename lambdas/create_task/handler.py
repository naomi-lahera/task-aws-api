import json
import os
import uuid
import boto3
from pydantic import ValidationError
from botocore.exceptions import ClientError
from models import CreateTaskRequest
from utils import create_response, ErrorMsg

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])

def lambda_handler(event, context):
    """
    Create a new task
    """
    try:
        body_str = event.get("body")
        if not body_str:
            return create_response(400, error=ErrorMsg.MISS_BODY.value)

        body = json.loads(body_str)
        task_request = CreateTaskRequest(**body)

        task_id = str(uuid.uuid4())
        item = {
            "taskId": task_id,
            "title": task_request.title,
            "description": task_request.description,
            "status": task_request.status
        }

        table.put_item(Item=item)

        return create_response(201, data=item)
    
    except ClientError as e:
        return create_response(400, error=e.response["Error"]["Message"])
    
    except ValidationError as e:
        error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return create_response(400, error="; ".join(error_messages))
    
    except Exception as e:
        return create_response(500, error=str(e))

