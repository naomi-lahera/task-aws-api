"""
Utility functions for Lambda handlers
"""
import json
from typing import Any, Optional, Dict
from enum import Enum

def create_response(
    status_code: int,
    data: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a standardized Lambda response
    """
    body = {}
    
    if data:
        body["data"] = data
    
    if error:
        body["error"] = error
    
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }

class ErrorMsg(Enum):
    MISS_BODY="Request body is required for update"
    VALIDATION_REQ="Validation error in request data"
    NOT_FOUND="Task not found"
    MISS_ID="Missing or invalid taskId in path parameters"
    NO_FIELDS_TO_UPDATE="No fields to update"
