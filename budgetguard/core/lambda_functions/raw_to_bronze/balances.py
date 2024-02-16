from budgetguard.main import run
from loguru import logger


def lambda_handler(event, context):
    logger.info("Starting raw to bronze balances pipeline lambda..")
    task = "raw_to_bronze_balances"
    partition_id = event["partition_id"]
    logger.info(f"Running task: {task} for partition: {partition_id}")
    run(task, partition_id)
    logger.info(f"Finished running task: {task} for partition: {partition_id}")
