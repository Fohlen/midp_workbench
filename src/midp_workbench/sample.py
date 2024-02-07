from pathlib import Path

import boto3
import numpy

from tqdm import tqdm

from src.midp_workbench.parser import load_sample

HBN_FOLDER_BASE = "data/Projects/HBN/EEG"


def sample_objects_for_participant_ids(
        bucket: boto3.session.Session.resource,
        ids: list[str]
) -> list[boto3.session.Session.resource]:
    objects = []
    for participant_id in tqdm(ids):
        objects.extend([
            obj for obj in bucket.objects.filter(
                Prefix=f"{HBN_FOLDER_BASE}/{participant_id}/Eyetracking/txt/{participant_id}"
            ) if "Video" in obj.key and obj.key.endswith("_Samples.txt")
        ])
    return objects


def preprocess_sample(
        obj: boto3.session.Session.resource,
        bucket_name: str,
        client: boto3.session.Session.client,
        output_dir: Path,
):
    """
    Downloads an object from a bucket and copies it to the output dir.
    :param obj: The object to fetch from S3.
    :param bucket_name: The name of the bucket to fetch
    :param client: The S3 client.
    :param output_dir: The output directory to copy to.
    """
    response_obj = client.get_object(Bucket=bucket_name, Key=obj.key)
    sample = load_sample(response_obj['Body'].read().decode('utf-8').splitlines())
    sample_output_path = output_dir / Path(obj.key).with_suffix(".npz").name
    numpy.savez_compressed(sample_output_path, **sample)
