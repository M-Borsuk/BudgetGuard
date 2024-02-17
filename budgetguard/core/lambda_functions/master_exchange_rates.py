from budgetguard.main import run
from loguru import logger


def lambda_handler(event, context):
    logger.info("Starting master exchange rates lambda..")
    task = "master_exchange_rates"
    partition_id = event["partition_id"]
    logger.info(f"Running task: {task} for partition: {partition_id}")
    run(task, partition_id)
    response = {
        "partition_id": partition_id,
    }
    logger.info(f"Finished running task: {task} for partition: {partition_id}")
    return response
