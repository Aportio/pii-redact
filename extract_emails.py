# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Tool to pre-process bulk import files into JSON
"""

import json
from typing import Optional
import uuid

from import_handlers import (
    VALID_FIELDS,
    import_spreadsheet,
    import_pst,
)


def get_aruments() -> dict:
    # create parser
    parser = argparse.ArgumentParser(description=f"Bulk email import {VERSION}")

    # add arguments to the parser
    parser.add_argument("file", help="File to process")
    parser.add_argument(
        "-b", "--bucket", help="S3 bucket to store output", default="pst-emails-storage"
    )
    parser.add_argument(
        "-p",
        "--bucket_prefix",
        help="S3 directory to store output. Defaults to customer id",
    )
    parser.add_argument(
        "-m", "--map", help="Define mappings for input fields", action="append"
    )

    # parse the arguments
    args = parser.parse_args()
    return args


def default_mapping() -> dict:
    """
    Return a default 1-1 mapping
    """
    mapping = {}
    for key in VALID_FIELDS:
        mapping[key] = [key]

    return mapping


def parse_field_mappings(raw_mappings: Optional[list]) -> dict:
    """
    Convert the list of mapping strings to a dict.
    """
    if not raw_mappings:
        return default_mapping()

    mapping = {}
    for item in raw_mappings:
        (key, value) = item.split("=")
        mapping[key.lower()] = value.split(",")

    return mapping


def extract_emails(file_name: str, export_dir: str, raw_mappings: Optional[list]):

    field_mappings = parse_field_mappings(raw_mappings)

    # Decide whether to use PST or CSV/Excel to import the file
    payloads = []
    if file_name.lower().endswith(".pst"):
        print(f"PST processing for {file_name}")
        payloads = import_pst(file_name)
    else:
        print(f"CSV processing for {file_name}")
        payloads = import_spreadsheet(file_name)

    item_count = 0
    for item_count, payload in enumerate(payloads):
        if item_count % 50 == 0:
            print(f"\nSaving payload {item_count+1}")
        print(".", end="", flush=True)

        filename = str(uuid.uuid4())
        path = f"data/export/{filename}.json"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)

    print(f"\nTotal payloads: {item_count+1}")
