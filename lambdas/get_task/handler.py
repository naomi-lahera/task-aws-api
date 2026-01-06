import os
import boto3
from botocore.exceptions import ClientError
from utils import create_response, ErrorMsg


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])

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
            return create_response(404, error=ErrorMsg.NOT_FOUND.value)
        
        return create_response(200, data=item)
    
    except ClientError as e:
        return create_response(400, error=e.response["Error"]["Message"])
    
    except Exception as e:
        return create_response(500, error=str(e))