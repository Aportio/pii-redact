# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Handle import from Microsoft PST files.
"""
import datetime
import email
import os
import subprocess
import tempfile
from typing import Tuple, List

from .utils import is_html, lowercase_keys


IGNORE_DIR_LIST = [
    "/Sent Items/",
    "/Recoverable Items/",
    "/Junk Email/",
    "/Attachments/",
]


def run_pffexport(*, pst_file_path: str, extraction_path: str) -> None:
    """
    Run the pffexport tool on the passed in file.
    """
    print(f"Extracting data from '{pst_file_path}'.")
    # Run pff-extractor on the PST file found in the config, and export it to tmp.
    pffexport_process = subprocess.run(
        ["pffexport", "-q", "-t", extraction_path, pst_file_path], capture_output=True
    )
    print(
        f"Completed extraction of data from '{pst_file_path}' to '{extraction_path}'."
    )
    if pffexport_process.returncode != 0:
        raise Exception(
            "there was an error running pffexport: "
            f"'{pffexport_process.stderr.decode('utf-8')}'"
        )


def get_required_data_from_extracted_pst(processed_pst_path: str) -> Tuple[dict, dict]:
    """
    Function to extract the paths for messages and headers.
    """
    print(f"Converting emails from '{processed_pst_path}'.")
    html_messages = {}
    text_messages = {}
    for current_dir_path, _, current_files in os.walk(processed_pst_path):
        # Ignore some folders, and try to only process the Inbox
        if any(ignore_dir in current_dir_path for ignore_dir in IGNORE_DIR_LIST):
            continue

        # Search for all folders that start with MessageXXX
        current_dir = current_dir_path.split("/")[-1]
        if current_dir.startswith("Message"):

            message_number = current_dir.split("Message")[-1]
            now = datetime.datetime.now().timestamp()
            unique_message_id = f"{message_number}__{now}"
            # Extract the to/from addresses and the subject from
            # the InternetHeaders.txt file, and get the email body from Message.txt or
            # Message.html
            if "InternetHeaders.txt" in current_files:
                if "Message.html" in current_files:
                    html_messages[unique_message_id] = {
                        "message": f"{current_dir_path}/Message.html",
                        "headers": f"{current_dir_path}/InternetHeaders.txt",
                    }
                elif "Message.txt" in current_files:
                    text_messages[unique_message_id] = {
                        "message": f"{current_dir_path}/Message.txt",
                        "headers": f"{current_dir_path}/InternetHeaders.txt",
                    }
    print(f"Completed converting emails from '{processed_pst_path}'.")
    return (html_messages, text_messages)


def read_file(file_path: str) -> str:
    """
    Read the passed in file and return the contents.
    """
    data = ""
    with open(file_path, "rb") as f:
        data = f.read()
    return data


def extract_headers_file(headers_file: str) -> dict:
    """
    Read the headers file and extract the required information from the file.
    """
    headers_data = read_file(file_path=headers_file)
    headers_dict = dict(email.message_from_string(headers_data.decode("utf-8")))
    return headers_dict


def get_json_from_email_data(*, headers: dict, message: str) -> dict:
    """
    Create a JSON-formatted payload from given email data.

    Note that by "JSON-formatted", we really just mean a dictionary.

    We need to fit the data into the cloudmailin format:
    {
        "headers": {
            "from"         : "someone@test.com",
            "sender"       : "someone@test.com",
            "date"         : "isoformat_datetime(YYYY-MM-DD HH:mm:ss TZ)",
            "to"           : "someone-else@test.com",
            "message_id"   : "<some_unique_id>",
            "subject"      : "Test email subject",
            "content_type" : "text/plain; charset=\"utf-8\""
        },
        "envelope"    : {},
        "plain"       : "This is a test email body",
        "attachments" : []
    }

    Returns the JSON-formatted payload.

    """
    lowercase_keys(headers, ["message-id", "to", "from", "cc", "date", "subject"])
    # These values come from the email headers, since they aren't available
    # from the message object.
    now = datetime.datetime.now()
    message_id = headers.get(
        "message-id", f"<{now.timestamp()}_pst_missing_message_id>"
    )
    recipient = headers.get("to", "analysis@aportio-analysis.com")
    sender = headers.get("from", "client@aportio-analysis.com")
    cc = headers.get("cc", "")
    date = headers.get("date", now.isoformat())
    subject = headers.get("subject", "-")

    email_body = message.decode(encoding="utf-8", errors="replace")
    email_plain = ""
    email_html = ""
    content_type = ""

    # Check for start and end HTML tags in the email
    if is_html(email_body):
        email_html = email_body
        content_type = 'text/html; charset="utf-8"'
    else:
        email_plain = email_body
        content_type = 'text/plain; charset="utf-8"'

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

    return json_body


def process_messages(message_dict: dict) -> List[dict]:
    """
    Get data from all the messages in the dict, then create the json payload.
    """
    print("Transforming emails into payloads.")
    messages_payloads = []
    for _, message_paths in message_dict.items():
        message = read_file(file_path=message_paths["message"])
        headers = extract_headers_file(headers_file=message_paths["headers"])
        message_json = get_json_from_email_data(headers=headers, message=message)
        messages_payloads.append(message_json)
    print(
        f"Completed transforming emails into payloads. Total {len(messages_payloads)}"
    )
    return messages_payloads


def import_pst(pst_file_location: str) -> list:
    """
    Import emails from a PST file.
    """
    with tempfile.TemporaryDirectory() as extraction_path:
        # Now extract the PST file
        try:
            run_pffexport(
                pst_file_path=pst_file_location, extraction_path=extraction_path
            )
            extraction_path += ".export/"
            html_data, text_data = get_required_data_from_extracted_pst(
                processed_pst_path=extraction_path
            )
            email_list = []
            email_list.extend(process_messages(message_dict=html_data))
            email_list.extend(process_messages(message_dict=text_data))
        except Exception as e:
            raise e

    return email_list
