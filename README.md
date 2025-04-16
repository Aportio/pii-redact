# PII Redact

**pii-redact** is a lightweight Python package designed to remove Personally Identifiable Information (PII) from emails presented in PST/CSV file.

It uses the [scrubadubdub](https://github.com/kylemclaren/scrub), which leverages advanced Machine Learning algorithms to detect PII and provides multiple levels of scrubbing to ensure optimal anonymization of sensitive information, safeguarding user privacy.

To provide customization of the [Spacy language model](https://spacy.io/models/en) used for processing,
we have copied the original [scrub.py](https://github.com/kylemclaren/scrub/blob/master/scrubadubdub/scrub.py) file from [scrubadubdub](https://github.com/kylemclaren/scrub).
Our copy can be found as [vendor/scrub.py](./vendor/scrub.py).

## Environment
Download and install [uv](https://github.com/astral-sh/uv)
following the instructions on their [installation page](https://docs.astral.sh/uv/getting-started/installation/).

**uv** is an extremely fast Python package and project manager, written in Rust. We use uv to install a copy of Python, install the dependancies, and run our tool.

### PST Dependancy

In order to extract emails from a PST file before redacting personal identifiable information,
we use an external tool ``pffexport`` which is part of the Debian package [pff-tools](https://packages.debian.org/search?keywords=pff-tools). We are currently dependant on the specific format of the tool's output.

**This introduces an additional dependancy if you intend to process PST files.**
The tool will need to be run in a Linux environment, and have the ``pffexport`` command available. On a Debian based system, including Ubuntu, this is done using the system package manager:
```bash
sudo apt-get install pff-tools
```

## Installation
- Clone this Git repository.
- Run ```uv sync``` to install Python and the dependencies.

```bash
git clone git@github.com:Aportio/pii-redact.git
cd pii-redact
uv sync
```

### Example - Redact a PST file
Let's assume we have a PST file **pst_file.pst**, and we want to store the redacted json files to **redacted_files** directory

```bash
uv run main.py <location of pst_file.pst> -o <location of redacted_files directory>
```

## Key Features
- **Supports CSV and PST**
- **Customizable**: Choose different [language models as per your requirement.](https://spacy.io/models/en)

## Notes
- **PST**: The tool extracts emails from PST file and redacts any personal identifiable information and then stores the result as a json in the directory. Because PST is a proprietary MS format and there are no good Python tools to read the PST format, we are using another tool called ``pffexport``, to read the PST and convert to plain files we can process. For this reason, PST processing is currently limited to running in a [Linux environment with the ``pffexport`` tool installed](#pst-dependancy).

- **CSV**: CSV version can be run from anywhere (Windows, Mac, or Linux)`

## License
**pii-redact** is licensed under the MIT License. See  [LICENSE](./LICENSE) for more details.

Once the tool is installed, a full list of licenses for each dependancy is available by running...

```
uv run licensecheck
```
