from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    CfnOutput
)
from constructs import Construct

class S3RotateCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self, "ImageBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=False,
            auto_delete_objects=False,
            removal_policy=RemovalPolicy.RETAIN,)

        fn = _lambda.DockerImageFunction(
            self, "RotateFunction",
            code=_lambda.DockerImageCode.from_image_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "OUTPUT_PREFIX": "output/"
            },
            timeout=Duration.seconds(30),
            memory_size=512,)

        bucket.grant_read_write(fn)

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(fn),
            s3.NotificationKeyFilter(prefix="incoming/"))

        CfnOutput(self, "BucketName", value=bucket.bucket_name)
