#!/bin/bash

# Set the default values for pid and t
pid="20231230"
t="dummy"

# Parse command line arguments
while getopts ":pid:t:" opt; do
  case $opt in
    pid)
      pid="$OPTARG"
      ;;
    t)
      t="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Build the Docker image
docker build --no-cache -t pyspark_dev -f Dockerfile_dev .

# Run the Docker container with provided arguments
docker run --rm pyspark_dev \
  --master "local[1]" \
  --conf "spark.ui.showConsoleProgress=True" \
  --conf "spark.ui.enabled=False" \
  /job/budgetguard/main.py -t "$t" -pid "$pid"
