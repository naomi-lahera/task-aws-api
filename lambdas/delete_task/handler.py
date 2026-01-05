import os
import boto3
from utils import create_response, ErrorMsg
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])

def lambda_handler(event, context):
    try:
        task_id = event.get("pathParameters", {}).get("taskId")
        if not task_id:
            return create_response(400, error=ErrorMsg.MISS_ID.value)

        get_task_response = table.get_item(Key={"taskId": task_id})
        item = get_task_response.get("Item")

        if not item:
            return create_response(404, error=ErrorMsg.NOT_FOUND.value)        
        
        table.delete_item(Key={"taskId": task_id})
        
        return create_response(204)

    except ClientError as e:
        return create_response(400, error=e.response["Error"]["Message"])
    
    except Exception as e:
        return create_response(500, error=str(e))
    
    