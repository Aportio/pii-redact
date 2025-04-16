# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Tool to pre-process bulk import files into JSON
"""

import json
import uuid

from import_handlers import (
    import_pst,
    import_spreadsheet,
)


def extract_emails(file_name: str):
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
            print(f"\nSaving payload {item_count + 1}")
        print(".", end="", flush=True)

        filename = str(uuid.uuid4())
        path = f"data/export/{filename}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)

    print(f"\nTotal payloads: {item_count + 1}")
