from aws_cdk import Stack, CfnOutput
from aws_cdk import (
    aws_ecs as _ecs,
    aws_ecs_patterns as _ecs_patterns,
    aws_ec2 as _ec2,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_route53 as _route53,
    aws_certificatemanager as _acm,
)
from constructs import Construct
from .s3_stack import FairflowS3Stack
from .ecs_cluster_stack import FairflowECSClusterStack
from .rds_cluster_stack import FairflowRDSStack
from .vpc_stack import FairflowVPCStack


class FairflowMessageBrokerStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        cluster: FairflowECSClusterStack,
        vpc: FairflowVPCStack,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Message Broker
        message_broker = _ecs.FargateService(
            self,
            "budgetguard-fairflow-message-broker",
            cluster=cluster.cluster,
        )

        message_broker.enable_cloud_map(
            name="budgetguard-fairflow-message-broker-cloud-map-service",
        )

        _ecs.CloudMapNamespaceOptions(
            name="budgetguard-fairflow-message-broker-cloud-map-namespace",
            vpc=vpc.vpc,
        )

        # message_broker_hostname = f"budgetguard-fairflow-message-broker-cloud-map-service.{cloudmap_namespace_options.name}"  # noqa: E501

        message_broker_task = _ecs.FargateTaskDefinition(
            self,
            "message-broker-task",
            cpu=1024,
            memory_limit_mib=2048,
        )

        rabbitmq_container = message_broker_task.add_container(
            "rabbitmq_container",
            image=_ecs.ContainerImage.from_registry("rabbitmq:management"),
            logging=_ecs.LogDrivers.aws_logs(
                stream_prefix="fairflow-message-broker",
            ),
            health_check=_ecs.HealthCheck(
                command=["CMD", "rabbitmqctl", "status"]
            ),
        )

        rabbitmq_container.add_port_mappings(
            _ecs.PortMapping(container_port=5672)
        )

        rabbitmq_container.add_port_mappings(
            _ecs.PortMapping(container_port=15672)
        )

        rabbitmq_alb = _elbv2.ApplicationLoadBalancer(
            self,
            "budgetguard-fairflow-message-broker-alb",
            vpc=vpc,
            internet_facing=True,
        )

        CfnOutput(
            self,
            id="rabbitmq-alb-dns-name",
            value=f"http://{rabbitmq_alb.load_balancer_dns_name}",
        )

        rabbitmq_listener = rabbitmq_alb.add_listener(
            "rabbit-listener", port=80
        )

        message_broker.register_load_balancer_targets(
            _ecs.EcsTarget(
                container_name=rabbitmq_container.container_name,
                container_port=15672,
                new_target_group_id="rabbitmq-management-tg",
                listener=_ecs.ListenerConfig.application_listener(
                    rabbitmq_listener,
                ),
            )
        )

        rabbitmq_alb.connections.allow_to(
            message_broker.connections,
            _ec2.Port.tcp(15672),
            description="allow connection to rabbitmq management api",
        )

        message_broker.register_load_balancer_targets(
            _ecs.EcsTarget(
                container_name="message-broker",
                container_port=5672,
                new_target_group_id="budgetguard-fairflow-message-broker-target-group",  # noqa: E501
                listener=_ecs.ListenerConfig.application_listener(
                    rabbitmq_listener
                ),  # noqa: E501
            )
        )

        rabbitmq_alb.connections.allow_to(
            message_broker.connections,
            _ec2.Port.tcp(15672),
            description="allow connection to rabbitmq management api",
        )


class FairflowWebUIStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        bucket: FairflowS3Stack,
        cluster: FairflowECSClusterStack,
        rds_instance: FairflowRDSStack,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        web_task = _ecs.FargateTaskDefinition(
            self,
            "web-task",
            cpu=1024,
            memory_limit_mib=2048,
        )

        bucket.bucket.grant_read_write(web_task.task_role.grant_principal)

        web_task.add_container(
            "web",
            image=_ecs.ContainerImage.from_registry(
                "placeholdernamespace/placeholderimage:placeholderimageversion"
            ),
            logging=_ecs.LogDrivers.aws_logs(
                stream_prefix="fairflow-web",
            ),
        )

        hosted_zone = _route53.PublicHostedZone(
            self,
            "budgetguard-fairflow-web-ui-hosted-zone",
            zone_name="budgetguard-fairflow-web-ui-hosted-zone",
            comment="budgetguard-fairflow-web-ui-hosted-zone",
        )

        web_service = _ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "web-service",
            cluster=cluster,
            task_definition=web_task,
            desired_count=1,
            protocol=_elbv2.ApplicationProtocol.HTTPS,
            domain_zone=hosted_zone,
            domain_name="budgetguard-fairflow-web-ui-hosted-zone",
            certificate=_acm.DnsValidatedCertificate(
                self,
                "budgetguard-fairflow-web-ui-certificate",
                domain_name="budgetguard-fairflow-web-ui-hosted-zone",
                hosted_zone=hosted_zone,
            ),
        )

        web_service.target_group.configure_health_check(
            healthy_http_codes="200-399",
        )

        web_service.service.connections.allow_to(
            rds_instance,
            _ec2.Port.tcp(5432),
            description="Allow web service to access RDS",
        )
