# Task Management Service - AWS Serverless App

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/naomi-lahera/todo-aws-api.git)

A complete serverless application on AWS using AWS CDK with Python. Includes:
- **REST API** with API Gateway
- **Lambda functions** for task CRUD operations
- **DynamoDB** database
- **Lambda Layers** with shared dependencies
- **Automatic deployment**

## Setup Instructions

### Prerequisites

The following must be installed before proceeding:

- **Python 3.11+**
- **AWS CLI**
- **Node.js 14+**
- **AWS Account**: With configured credentials

### Step 1: Extract the Project

The project must be extracted from the .zip file. The extracted folder should be named `task-aws-api-main`. Once extracted, you must navigate into the project folder:

```bash
cd task-aws-api-main
```

### Step 2: Configure AWS Credentials

AWS credentials must be configured locally:

```bash
aws configure
```

When prompted, the following information must be provided:
- **AWS Access Key ID**: Your access key
- **AWS Secret Access Key**: Your secret key
- **Default region**: Example: `us-east-1`
- **Default output format**: Example: `json`

### Step 3: Create and Activate Virtual Environment

### Step 4: Install Project Dependencies

The project dependencies must be installed by running:

```bash
pip install -r requirements.txt
```

### Step 5: Install AWS CDK Globally (if not already installed)

```bash
npm install -g aws-cdk
```

### Step 6: Create Lambda Layer Dependencies

The Lambda layers must be created with specific dependencies built for the Lambda runtime environment. The following commands must be executed:

**Install Pydantic:**
```bash
pip install pydantic==2.9.2 -t lambdas/layers/dependencies/python --platform manylinux2014_x86_64 --only-binary=:all: --python-version 3.11 --implementation cp --upgrade
```

The following will be accomplished by these commands:
- Packages will be installed to `lambdas/layers/dependencies/python` directory

## How to Deploy the Solution

### Deploy Using CDK Commands

**Step 1: Synthesize the CloudFormation Template**

```bash
cdk synth
```

The CloudFormation template must be generated without deploying.

**Step 2: Deploy the Stack**

```bash
cdk deploy
```

The following must occur when deploying:
1. A summary of resources to be created must be shown
2. Confirmation must be requested (type `y` to confirm)
3. The stack must be deployed to the AWS account
4. Stack outputs must be displayed including API endpoint URL

## Cleanup

All AWS resources created by the stack must be removed by running:

```bash
cdk destroy
```

**Warning**: This action is irreversible and the following will be deleted:
- API Gateway
- Lambda functions
- DynamoDB table
- Lambda layers
- IAM roles and policies

**Important Note - DynamoDB Table Deletion**:

The DynamoDB table **will be deleted** when running `cdk destroy` because it is configured with:
- `RemovalPolicy.DESTROY`: Allows the table to be removed when the stack is destroyed
- `deletion_protection = False`: No protection against deletion

This configuration was chosen for **development environments** where resources can be easily recreated.

**For Production Environments**, the configuration must be changed to:
- `RemovalPolicy.RETAIN`: Keeps the table even when the stack is destroyed
- `deletion_protection = True`: Adds protection against accidental deletion

These changes must be made in the CDK stack definition before deploying to production to ensure data protection.

Confirmation must be provided by typing `y` when prompted.

## Testing the API

After deploying the stack successfully, the API Gateway endpoint will be displayed in the deployment output. Look for the output named `TaskAppStack.TasksApiEndpointxxxxxxxxx` which will provide a URL in the following format:

```
https://xxxxxxxxxx.execute-api.xxxxxxxxx.amazonaws.com/prod/
```

Concatenate `/tasks` to this base URL to form the API endpoint:

```
https://xxxxxxxxxx.execute-api.xxxxxxxxx.amazonaws.com/prod/tasks
```

### API Endpoints

The following endpoints are available for task management:

#### 1. Create a Task
- **Method**: `POST`
- **URL**: `https://xxxxxxxxxx.execute-api.xxxxxxxxx.amazonaws.com/prod/tasks`
- **Request Body**:
```json
{
  "title": "Task title",
  "description": "Task description",
  "status": "pending"
}
```
- **Valid Status Values**: `pending`, `in-progress`, `completed`
- **Response** (201 Created):
```json
{
  "taskId": "uuid-generated-id",
  "title": "Task title",
  "description": "Task description",
  "status": "pending"
}
```

#### 2. Get a Task
- **Method**: `GET`
- **URL**: `https://xxxxxxxxxx.execute-api.xxxxxxxxx.amazonaws.com/prod/tasks/{taskId}`
- **Response** (200 OK):
```json
{
  "taskId": "uuid-generated-id",
  "title": "Task title",
  "description": "Task description",
  "status": "pending"
}
```

#### 3. Update a Task
- **Method**: `PUT`
- **URL**: `https://xxxxxxxxxx.execute-api.xxxxxxxxx.amazonaws.com/prod/tasks/{taskId}`
- **Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "in-progress"
}
```
- **Response** (200 OK):
```json
{
  "taskId": "uuid-generated-id",
  "title": "Updated title",
  "description": "Updated description",
  "status": "in-progress"
}
```

#### 4. Delete a Task
- **Method**: `DELETE`
- **URL**: `https://xxxxxxxxxx.execute-api.xxxxxxxxx.amazonaws.com/prod/tasks/{taskId}`
- **Response** (204 No Content): Empty response