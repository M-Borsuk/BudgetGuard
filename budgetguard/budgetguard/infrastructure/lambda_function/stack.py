from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_ecr as _ecr
from aws_cdk import Aws, Duration
import typing
from constructs import Construct


class IngestionLambdaStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, image_name: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.build_lambda_func(self.get_lambda_image(image_name))

    def get_lambda_image(self, image_name: str):
        ecr_repository = _ecr.Repository.from_repository_attributes(
            self,
            id="ECR",
            repository_arn="arn:aws:ecr:{0}:{1}".format(
                Aws.REGION, Aws.ACCOUNT_ID
            ),
            repository_name=image_name,
        )
        ecr_image = typing.cast(
            "_lambda.Code", _lambda.EcrImageCode(repository=ecr_repository)
        )
        return ecr_image

    def build_lambda_func(self, lambda_image: _lambda.Code):
        self.prediction_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="IngestionLambda",
            function_name="IngestionLambda",
            code=lambda_image,
            timeout=Duration.seconds(300),
            memory_size=1024,
            handler=_lambda.Handler.FROM_IMAGE,
            runtime=_lambda.Runtime.FROM_IMAGE,
        )
