#!/bin/bash

# Parse command line arguments
while getopts p:t: flag
do
    case "${flag}" in
        p) partition=${OPTARG};;
        t) task=${OPTARG};;
    esac
done

# Build Docker image
docker build -t pyspark_dev -f Dockerfile_dev .

# Run Docker container
docker run --rm pyspark_dev \
  --master "local[1]" \
  --conf "spark.ui.showConsoleProgress=True" \
  --conf "spark.ui.enabled=False" \
  /job/budgetguard/main.py -t "$task" -pid "$partition"
