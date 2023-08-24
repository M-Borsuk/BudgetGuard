from aws_cdk import Stack, RemovalPolicy, CfnOutput
from aws_cdk import (
    aws_s3 as _s3,
)
from constructs import Construct


class FairflowS3Stack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket
        bucket = _s3.Bucket(
            self,
            "budgetguard-fairflow-s3",
            bucket_name="budgetguard-fairflow-s3",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        CfnOutput(
            self,
            "s3-log-bucket",
            value=f"https://s3.console.aws.amazon.com/s3/buckets/{bucket.bucket_name}",  # noqa: E501
            description="where worker logs are written to",
        )

        self.bucket = bucket
