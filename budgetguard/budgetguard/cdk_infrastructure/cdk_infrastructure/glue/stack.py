from aws_cdk import Stack, Aws
from aws_cdk import aws_glue as glue
from constructs import Construct


class GlueDataCatalogStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a Glue Data Catalog database
        database = glue.CfnDatabase(
            self,
            "budget-guard-ingest-database",
            catalog_id=Aws.ACCOUNT_ID,
            database_input={
                "name": "budget-guard-ingest-database",
                "description": "AWS Glue Database for ingestion",
            },
        )

        self.database = database


class GlueCrawlersStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a Glue Crawler
        crawler = glue.CfnCrawler(
            self,
            "budget-guard-ingest-crawler",
            name="budget-guard-ingest-crawler",
            role=f"arn:aws:iam::{Aws.ACCOUNT_ID}:role/service-role/AWSGlueServiceRole",  # noqa
            database_name="budget-guard-ingest-database",
            targets={"s3Targets": [{"path": "s3://budget-guard-ingest"}]},
        )

        glue.CfnTrigger(
            self,
            "budget-guard-ingest-crawler-trigger",
            name="budget-guard-ingest-crawler-trigger",
            type="SCHEDULED",
            actions=[{"crawlerName": crawler.name}],
            schedule="cron(0 0 * * ? *)",  # Example: Daily at midnight
        )

        # Define a Glue Table using the output from the Crawler
        glue.CfnTable(
            self,
            "budget-guard-ingest-balances",
            database_name="budget-guard-ingest-database",
            catalog_id=Aws.ACCOUNT_ID,
            table_input={
                "name": "budget-guard-ingest-balances",
                "tableType": "EXTERNAL_TABLE",
                "parameters": {"classification": "json"},
                "storageDescriptor": {
                    "columns": [
                        {"name": "balances", "type": "array"},
                        {"name": "partition_id", "type": "string"},
                        {"name": "account_id", "type": "string"},
                    ],
                    "location": "s3://budget-guard-ingest/balances/",
                    "partitionKeys": [
                        {"name": "partition_id", "type": "string"},
                        {"name": "account_id", "type": "string"},
                    ],
                },
            },
        )

        glue.CfnTable(
            self,
            "budget-guard-ingest-details",
            database_name="budget-guard-ingest-database",
            catalog_id=Aws.ACCOUNT_ID,
            table_input={
                "name": "budget-guard-ingest-details",
                "tableType": "EXTERNAL_TABLE",
                "parameters": {"classification": "json"},
                "storageDescriptor": {
                    "columns": [
                        {"name": "details", "type": "struct"},
                        {"name": "partition_id", "type": "string"},
                        {"name": "account_id", "type": "string"},
                    ],
                    "location": "s3://budget-guard-ingest/details/",
                    "partitionKeys": [
                        {"name": "partition_id", "type": "string"},
                        {"name": "account_id", "type": "string"},
                    ],
                },
            },
        )

        glue.CfnTable(
            self,
            "budget-guard-ingest-metadata",
            database_name="budget-guard-ingest-database",
            catalog_id=Aws.ACCOUNT_ID,
            table_input={
                "name": "budget-guard-ingest-metadata",
                "tableType": "EXTERNAL_TABLE",
                "parameters": {"classification": "json"},
                "storageDescriptor": {
                    "columns": [
                        {"name": "id", "type": "string"},
                        {"name": "created", "type": "string"},
                        {"name": "last_accessed", "type": "string"},
                        {"name": "iban", "type": "string"},
                        {"name": "institution_id", "type": "string"},
                        {"name": "status", "type": "string"},
                        {"name": "owner_name", "type": "string"},
                        {"name": "partition_id", "type": "string"},
                        {"name": "account_id", "type": "string"},
                    ],
                    "location": "s3://budget-guard-ingest/metadata/",
                    "partitionKeys": [
                        {"name": "partition_id", "type": "string"},
                        {"name": "account_id", "type": "string"},
                    ],
                },
            },
        )

        glue.CfnTable(
            self,
            "budget-guard-ingest-transactions",
            database_name="budget-guard-ingest-database",
            catalog_id=Aws.ACCOUNT_ID,
            table_input={
                "name": "budget-guard-ingest-transactions",
                "tableType": "EXTERNAL_TABLE",
                "parameters": {"classification": "json"},
                "storageDescriptor": {
                    "columns": [
                        {"name": "transactions", "type": "struct"},
                        {"name": "partition_id", "type": "string"},
                        {"name": "account_id", "type": "string"},
                    ],
                    "location": "s3://budget-guard-ingest/transactions/",
                    "partitionKeys": [
                        {"name": "partition_id", "type": "string"},
                        {"name": "account_id", "type": "string"},
                    ],
                },
            },
        )
