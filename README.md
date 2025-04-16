# PII Redact

**pii-redact** is a lightweight Python package designed to remove Personally Identifiable Information (PII) from emails presented in PST/CSV file. It uses scrubadubdub which leverages advanced Machine Learning algorithms to detect PII and provides multiple levels of scrubbing to ensure optimal anonymization of sensitive information, safeguarding user privacy.

## Environment 
Set up **uv** https://github.com/astral-sh/uv

**uv** is an extremely fast Python package and project manager, written in Rust. We use uv to run our tool

## Installation
Install from source. Run ```uv sync``` to install the dependencies

```bash
git clone git@github.com:Aportio/pii-redact.git
cd pii-redact
uv sync
```
### Example
Let's assume we have a PST file **pst_file.pst**, and we want to store the redacted json files to **redacted_files** directory
```
uv run main.py <location of pst_file.pst> -o <location of redacted_files directory>
```

## Key Features
- **Supports CSV and PST**
- **Customizable**: Choose different language models as per your requirement. https://spacy.io/models/en

## Notes
- **PST**: The tool extracts emails from PST file and redacts any personal identifiable information and then stores the result as a json in the directory. For PST, because that is a proprietary MS format, and hard to deal with, and there are no good Python tools to read the PST format - for these reasons, we are using another tool  called pffexport, to read the PST and convert to plain files we can process.We are using a Linux pffexport tool.
- **CSV**: CSV version can be run from anywhere (Windows, Mac, or Linux)`

## License
pii-redact is licensed under the MIT License. See  [LICENSE](./LICENSE) for more details.
