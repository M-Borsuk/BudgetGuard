docker run --name budgetguard_pyspark --rm --mount type=bind,source="$(pwd)",target=/opt/application pyspark_dev driver local:///opt/application/budgetguard/budgetguard/scripts/test_pyspark_setup.py
