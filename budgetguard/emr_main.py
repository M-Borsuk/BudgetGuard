from budgetguard.core.pipelines.pipeline import Pipeline
import sys


def run_task(pipeline: Pipeline):
    pipeline.run()


def run(task: str, partition_id: str):
    if task == "ingest_account_data":
        from budgetguard.core.pipelines.ingest_account_data import (
            IngestAccountData,
        )

        pipeline = IngestAccountData(partition_id)
    elif task == "bronze_to_silver_balances":
        from budgetguard.core.pipelines.bronze_to_silver.balances_pipeline import (
            BronzeToSilverBalancesPipeline,
        )

        pipeline = BronzeToSilverBalancesPipeline(partition_id)
    elif task == "bronze_to_silver_details":
        from budgetguard.core.pipelines.bronze_to_silver.details_pipeline import (
            BronzeToSilverDetailsPipeline,
        )

        pipeline = BronzeToSilverDetailsPipeline(partition_id)
    elif task == "bronze_to_silver_transactions":
        from budgetguard.core.pipelines.bronze_to_silver.transactions_pipeline import (
            BronzeToSilverTransactionsPipeline,
        )

        pipeline = BronzeToSilverTransactionsPipeline(partition_id)
    elif task == "bronze_to_silver_metadata":
        from budgetguard.core.pipelines.bronze_to_silver.metadata_pipeline import (
            BronzeToSilverMetadataPipeline,
        )

        pipeline = BronzeToSilverMetadataPipeline(partition_id)
    else:
        raise ValueError(f"Unknown task: {task}")
    run_task(pipeline)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
