import os
import boto3
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger
from utils import create_response, ErrorMsg


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])

logger = Logger()

def lambda_handler(event, context):
    """
    Get a task by taskId
    """
    try:
        task_id = event.get("pathParameters", {}).get("taskId")
        if not task_id or not task_id.strip():
            return create_response(400, error=ErrorMsg.MISS_ID.value)
        
        response = table.get_item(Key={"taskId": task_id})
        item = response.get("Item")

        if not item:
            return create_response(404, message=ErrorMsg.NOT_FOUND.value)
        
        return create_response(200, data=item)
    
    except ClientError as e:
        logger.error(f"DynamoDB ClientError: {e.response['Error']['Message']}")
        return create_response(400, error=e.response["Error"]["Message"])
    
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        return create_response(500, error=str(e))