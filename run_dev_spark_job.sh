#!/bin/bash

# Build Docker image
docker build -t pyspark_dev -f Dockerfile_dev .

# Run Docker container
docker run --rm pyspark_dev \
  --master "local[1]" \
  --conf "spark.ui.showConsoleProgress=True" \
  --conf "spark.ui.enabled=False" \
  /job/budgetguard/main.py -t "master_exchange_rates" -pid "20240216"
