from aws_cdk import Stack
from aws_cdk import (
    aws_ecs as _ecs,
)
from .vpc_stack import FairflowVPCStack
from constructs import Construct


class FairflowECSClusterStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc: FairflowVPCStack,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        cloud_map_namespace = _ecs.CloudMapNamespaceOptions(
            name="budgetguard-fairflow-ecs-cloud-map-namespace",
            vpc=vpc.vpc,
        )

        # Create ECS Cluster
        cluster = _ecs.Cluster(
            self,
            "budgetguard-fairflow-ecs-cluster",
            cluster_name="budgetguard-fairflow-ecs-cluster",
            vpc=vpc.vpc,
            default_cloud_map_namespace=cloud_map_namespace,
        )

        self.cluster = cluster
