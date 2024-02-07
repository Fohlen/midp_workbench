#!/usr/bin/python3
import argparse
from functools import partial
from pathlib import Path

import boto3
from botocore import UNSIGNED

from tqdm.contrib.concurrent import thread_map

from src.midp_workbench.sample import preprocess_sample, sample_objects_for_participant_ids

HBN_S3_BUCKET = "fcp-indi"


def main(
        participant_ids: list[str],
        output_dir: Path,
        max_workers: int
):
    """
    Downloads and pre-processes the specified participants into the given output dir.
    :param participant_ids: The participant ids to use.
    :param output_dir: The output dir to use.
    :param max_workers: The number of workers to use.
    """

    config = boto3.session.Config(signature_version=UNSIGNED)
    s3 = boto3.resource('s3', config=config)
    client = boto3.client('s3', config=config)
    bucket = s3.Bucket(HBN_S3_BUCKET)

    print(f"Fetching sample keys for {len(participant_ids)} participants")

    sample_objects = sample_objects_for_participant_ids(bucket, participant_ids)
    print(f"Downloading {len(sample_objects)} samples")
    download_fn = partial(preprocess_sample, client=client, bucket_name=HBN_S3_BUCKET, output_dir=output_dir)
    thread_map(download_fn, sample_objects, max_workers=max_workers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "participant_id", nargs="+"
    )
    parser.add_argument(
        "-o", "--output-dir", nargs="?", type=Path, default=Path.cwd() / "data" / "preprocessed_samples"
    )
    parser.add_argument(
        "--max-workers", nargs="?", type=int, default=4
    )
    args = parser.parse_args()

    main(args.participant_id, args.output_dir, args.max_workers)
