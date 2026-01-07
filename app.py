#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws.aws_stack import TaskAppStack

app = cdk.App()
TaskAppStack(app, "TaskAppStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'), 
        region=os.getenv('CDK_DEFAULT_REGION')),
    )

app.synth()
