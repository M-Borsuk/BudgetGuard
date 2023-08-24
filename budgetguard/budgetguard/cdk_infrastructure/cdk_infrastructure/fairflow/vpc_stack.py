from aws_cdk import Stack
from aws_cdk import (
    aws_ec2 as _ec2,
)
from constructs import Construct


class FairflowVPCStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC
        vpc = _ec2.Vpc(self, "budgetguard-fairflow-vpc")

        self.vpc = vpc
