import os
import json
import boto3
from utils import create_response, ErrorMsg
from pydantic import ValidationError
from models import UpdateTaskRequest
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])

def lambda_handler(event, context):
    """
    Update task
    """
    try:
        task_id = event.get("pathParameters", {}).get("taskId")     
        if not task_id:
            return create_response(400, error=ErrorMsg.MISS_ID.value)

        get_task_response = table.get_item(Key={"taskId": task_id})
        item = get_task_response.get("Item")

        if not item:
            return create_response(404, error=ErrorMsg.NOT_FOUND.value)

        body_str = event.get("body")
        if not body_str:
            return create_response(400, error=ErrorMsg.MISS_BODY.value)
        
        body = json.loads(body_str)       
        task_request = UpdateTaskRequest(**body)

        update_expression = []
        expression_values = {}
        expression_names = {}

        for field, value in task_request.model_dump(exclude_none=True).items():
            update_expression.append(f"#{field}=:{field}")
            expression_values[f":{field}"] = value
            expression_names[f"#{field}"] = field

        if not update_expression:
            return create_response(400, message=ErrorMsg.NO_FIELDS_TO_UPDATE.value)

        update_params = {
            "Key": {"taskId": task_id},
            "UpdateExpression": "SET " + ", ".join(update_expression),
            "ExpressionAttributeValues": expression_values,
            "ReturnValues": "ALL_NEW"
        }
        
        if expression_names:
            update_params["ExpressionAttributeNames"] = expression_names

        response = table.update_item(**update_params)

        return create_response(200, data=response["Attributes"])

    except ClientError as e:
        return create_response(400, error=e.response["Error"]["Message"])

    except ValidationError as e:
        error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return create_response(400, error="; ".join(error_messages))
    
    except Exception as e:
        return create_response(500, error=str(e))
