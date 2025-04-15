# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

import argparse

from version import VERSION


def get_aruments() -> dict:
    # create parser
    parser = argparse.ArgumentParser(description=f"PII Email Redactor {VERSION}")

    # add arguments to the parser
    parser.add_argument("file", help="File to process")
    parser.add_argument(
        "-o", "--out", help="Output directory", default="redacted-emails"
    )
    parser.add_argument(
        "-m", "--map", help="Define mappings for input fields", action="append"
    )

    # parse the arguments
    args = parser.parse_args()
    return args


def main():
    """ """
    # Get the PST or CSV file from the directory
    # Extract the email content from the file
    # Now loop through the files in the exported directory
    # Redact the email content from them
    # Save all the redacted data in a separate directory
    print("")


if __name__ == "__main__":
    main()
