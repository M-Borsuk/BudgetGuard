from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_ecr as _ecr
from aws_cdk import aws_iam as _iam
from aws_cdk import Aws, Duration
from constructs import Construct


class RawToBronzeLambdaStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        table_name: str,
        image_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.build_lambda_func(
            self.get_lambda_image(image_name, table_name), table_name
        )

    def get_lambda_image(self, image_name: str, table_name: str):
        ecr_repository = _ecr.Repository.from_repository_attributes(
            self,
            id="ECR",
            repository_arn="arn:aws:ecr:{0}:{1}:repository".format(
                Aws.REGION, Aws.ACCOUNT_ID
            ),
            repository_name=image_name,
        )
        ecr_image = _lambda.DockerImageCode.from_ecr(
            repository=ecr_repository,
            tag_or_digest="latest",
            cmd=[
                f"budgetguard.core.lambda_functions.raw_to_bronze.{table_name}.lambda_handler"  # noqa
            ],
            entrypoint=["python", "-m", "awslambdaric"],
        )
        return ecr_image

    def build_lambda_func(self, lambda_image: _lambda.Code, table_name: str):
        raw_to_bronze_lambda = _lambda.DockerImageFunction(
            scope=self,
            id=f"RawToBronzeLambda{table_name.title()}",
            function_name=f"RawToBronzeLambda{table_name.title()}",
            code=lambda_image,
            timeout=Duration.seconds(300),
            memory_size=1024,
        )
        raw_to_bronze_lambda.add_to_role_policy(
            _iam.PolicyStatement(
                actions=["s3:*"],
                resources=[
                    "arn:aws:s3:::budget-guard-ingest/*",
                    "arn:aws:s3:::budget-guard-ingest",
                    "arn:aws:s3:::budget-guard-bronze/*",
                    "arn:aws:s3:::budget-guard-bronze",
                ],
                effect=_iam.Effect.ALLOW,
            )
        )
