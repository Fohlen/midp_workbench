midp_workbench
--------------

The MIDP workbench is a utility library to download and preprocess eye tracking data from the [Multimodal Resource for Studying Information Processing in the Developing Brain](http://fcon_1000.projects.nitrc.org/indi/cmi_eeg/).

# Installation

TBD

# Usage

You can invoke the package from the command-line:

```
fetch-eeg-samples -o output_folder/ ID1
```

It will produce a [NPZ archive](https://numpy.org/doc/stable/reference/generated/numpy.savez.html) of all the variables found in the original recording.
Consequently one can use e.g. [REMoDNaV](https://github.com/psychoinformatics-de/remodnav) to post-process this data.

One can also bulk-download multiple items at once using `xargs`, e.g. download blocks of 100 participants at once:

```
cat my_list_of_participants.txt # should contain one ID per line
xargs fetch-eeg-samples -o output_folder < my_list_of_participants.txt
```

# Invoking programmatically

You can also re-use this library in your own projects. The API is straightforward from [fetch-eeg-samples](src/midp_workbench/fetch_eeg_samples.py).
