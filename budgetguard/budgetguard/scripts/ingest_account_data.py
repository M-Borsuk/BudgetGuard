import argparse
import sys
import os

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))
from pipelines.ingest_account_data import IngestAccountData  # noqa: E402


parser = argparse.ArgumentParser()

parser.add_argument(
    "-pid",
    "--partition-id",
    help="The partition of the datalake to read from.",
    type=str,
    required=True,
)

if __name__ == "__main__":
    args = parser.parse_args()
    pipeline = IngestAccountData(args.partition_id)
    pipeline.run()
