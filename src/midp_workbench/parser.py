import re
from typing import Mapping

import numpy


IS_DIGIT = re.compile(r'^-?\d+$')
IS_FLOAT = re.compile(r'^-?(\d*\.\d+)|(\d+\.\d*)$')
# This is a magic number that varies between versions of iView
NUM_MIN_COLUMNS = 20


def dtype_from_value(value: str) -> type:
    """
    Returns the dtype for this value.
    :param value: an example value for this type of data.
    :return: the data type to be used with e.g. numpy's dtype
    """
    if IS_DIGIT.match(value):
        return int
    elif IS_FLOAT.match(value):
        return float
    return str


def load_sample(sample_file: list[str]) -> Mapping[str, numpy.ndarray]:
    """
    Returns a mapping of all columns of a sample file.
    :param sample_file: The sample file to be loaded.
    :return: Mapping of header column to a numpy arrays of values with the correct dtype.
    """
    rows = [
        row for line in sample_file
        if (row := line.split("\t")) is not None and len(row) >= NUM_MIN_COLUMNS
    ]
    header = rows.pop(0)  # this is the header
    dtypes = [dtype_from_value(value) for value in rows[0]]
    return {
        header: numpy.array(value, dtype=dtype)
        for header, dtype, value in zip(header, dtypes, zip(*rows))
    }
