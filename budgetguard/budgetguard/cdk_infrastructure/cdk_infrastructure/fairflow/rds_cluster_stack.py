from aws_cdk import Stack, RemovalPolicy, SecretValue
from aws_cdk import (
    aws_rds as _rds,
    aws_ec2 as _ec2,
)
from .vpc_stack import FairflowVPCStack
from constructs import Construct


class FairflowRDSStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        master_username: str,
        master_password: str,
        vpc: FairflowVPCStack,
        allocated_storage: int,
        database_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create RDS Cluster
        rds_cluster = _rds.DatabaseCluster(
            self,
            "budgetguard-fairflow-rds-cluster",
            engine=_rds.DatabaseInstanceEngine.POSTGRES,
            allocated_storage=allocated_storage,
            database_name=database_name,
            master_username=master_username,
            master_user_password=SecretValue.plain_text(master_password),
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
            delete_automated_backups=True,
            instance_type=_ec2.InstanceType("t3.micro"),
        )

        self.rds_cluster = rds_cluster
