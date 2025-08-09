#!/usr/bin/env python3
import os

import aws_cdk as cdk

from s3_rotate_cdk.s3_rotate_cdk_stack import S3RotateCdkStack


app = cdk.App()

S3RotateCdkStack(
    app, "S3RotateCdkStack",
    env=cdk.Environment(
        account="009160047123",
        region="ap-southeast-2"
    )
)

app.synth()
