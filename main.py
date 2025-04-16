# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

import argparse
import os
import json

from version import VERSION
from pathlib import Path
from redact_emails import redact_text
from extract_emails import extract_emails

EXPORT_DIR = "data/export/"
HEADERS_WITH_PII = [
    "from",
    "sender",
    "to",
    "cc",
    "subject",
]


def get_aruments() -> dict:
    # create parser
    parser = argparse.ArgumentParser(description=f"PII Email Redactor {VERSION}")

    # add arguments to the parser
    parser.add_argument("file", help="File to process(PST/CSV)")
    parser.add_argument(
        "-o", "--outdir", help="Output directory", default="redacted-emails"
    )
    # parse the arguments
    args = parser.parse_args()
    return args


def redact_payload(payload: dict) -> dict:
    """
    Redact all PII in the payload.

    payload structure looks like this:
    json_body = {
        "headers": {
            "from": sender,
            "sender": sender,
            "date": date,
            "to": recipient,
            "cc": cc,
            "message_id": message_id.strip("\r\n "),
            "subject": subject,
            "content_type": content_type,
        },
        "envelope": {},
        "plain": email_plain,
        "html": email_html,
        "attachments": [],
    }
    """
    redacted_payload = payload
    for key, value in payload.get("headers", {}).items():
        if key in HEADERS_WITH_PII:
            redacted_payload["headers"][key] = redact_text(
                payload.get("headers", {}).get(key, "")
            )
    redacted_payload["plain"] = redact_text(payload.get("plain", ""))
    redacted_payload["html"] = redact_text(payload.get("html", ""))
    return redacted_payload


def main():
    """ """
    # Get the arguments.
    args = get_aruments()

    # Get the PST location
    file_name = args.file

    # Redacted email directory
    redacted_dir = args.outdir

    # Extract the email content from the file
    extract_emails(file_name=file_name)

    # Now loop through the files in the exported directory
    # Redact the email content from them
    # Save all the redacted data in a separate directory
    pathlist = Path(EXPORT_DIR).rglob("*.json")
    for path in pathlist:
        with open(str(path), "r", encoding="utf-8") as f:
            payload = json.load(f)
            redacted_payload = redact_payload(payload)
            filename = os.path.basename(f.name)
            path = f"data/{redacted_dir}/{filename}"
            with open(path, "w", encoding="utf-8") as outf:
                json.dump(redacted_payload, outf, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
