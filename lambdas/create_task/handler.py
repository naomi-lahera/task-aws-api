import json
import os
import uuid
import boto3
from pydantic import ValidationError
import logging
from botocore.exceptions import ClientError
from models import CreateTaskRequest
from utils import create_response, ErrorMsg
from aws_lambda_powertools import Logger

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])

logger = Logger()

@logger.inject_lambda_context
def lambda_handler(event, context):
    """
    Create a new task
    """
    try:
        body_str = event.get("body")
        if not body_str:
            logger.error(ErrorMsg.MISS_BODY.value)
            return create_response(400, message=ErrorMsg.MISS_BODY.value)

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

        logger.info(f"Task created successfully: {task_id}")
        return create_response(201, data=item)
    
    except ClientError as e:
        logger.error(f"DynamoDB ClientError: {e.response['Error']['Message']}")
        return create_response(400, error=e.response["Error"]["Message"])
    
    except ValidationError as e:
        error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        logger.error(f"ValidationError: {'; '.join(error_messages)}")
        return create_response(400, error="; ".join(error_messages))
    
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        return create_response(500, error=str(e))

