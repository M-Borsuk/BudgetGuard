import os
from aws_cdk import App
from aws_cdk import Environment
from cdk_infrastructure.lambdas.raw_to_bronze_stack import (
    RawToBronzeLambdaStack,
)
from cdk_infrastructure.lambdas.ingestion_stack import IngestionLambdaStack
from cdk_infrastructure.s3_buckets.stack import S3DeployStack
from cdk_infrastructure.glue.stack import (
    GlueDataCatalogStack,
    GlueCrawlersStack,
)
from cdk_infrastructure.s3_buckets.constants import BUCKET_NAMES
from dotenv import load_dotenv

load_dotenv()

env = Environment(
    account=os.environ.get("AWS_ACCOUNT_ID"),
    region=os.environ.get("AWS_REGION_NAME"),
)

app = App()

IngestionLambdaStack(
    app, "LambdaIngestionStack", image_name="budget-guard", env=env
)

RawToBronzeLambdaStack(
    app, "LambdaRawToBronzeStack", image_name="budget-guard", env=env
)

for bucket_name in BUCKET_NAMES:
    S3DeployStack(app, f"{bucket_name}Stack", bucket_id=bucket_name, env=env)

catalog = GlueDataCatalogStack(app, "GlueDataCatalogStack", env=env)

GlueCrawlersStack(
    app,
    "GlueCrawlersStack",
    env=env,
)

app.synth()