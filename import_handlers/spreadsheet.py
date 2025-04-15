# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Handle import from spreadsheet files.
"""

import pandas

from .utils import is_html, validate_email

# Fields that we absolutely must have in a given spreadsheet file.
REQUIRED_FIELDS = ["unique_id", "subject", "body", "date"]
IMPORT_FIELDS = REQUIRED_FIELDS + ["to", "from"]

# Filetypes that we support reading from.
SUPPORTED_FILETYPE_READERS = {"csv": pandas.read_csv, "xlsx": pandas.read_excel}

# The email list is global, so convert_to_json can access it inside the pandas loop
email_list = []


def read_spreadsheet_emails(filename):
    """
    Read data from the given spreadsheet file.

    Note that a "spreadsheet file" can refer to any spreadsheet-like file, e.g.
    a CSV file or an Excel file.

    Support for various spreadsheet files is outlined in the
    SUPPORTED_FILETYPE_READERS global dict.

    Note that this function assumes the filename has a file extension at the
    end, e.g. ".csv" or ".xlsx".

    Parameters
    ----------
    filename : str
        The name of the file to read from.

    """
    # Split the filename on the dot, so we get the name and extension.
    # e.g. "my_file.csv" -> ["my_file", "csv"]
    filename_parts = filename.split(".")
    if len(filename_parts) < 2:
        raise Exception(
            "No file extension detected. Make sure the filename contains a file "
            "extension, e.g. '.csv' or '.xlsx'"
        )
    file_ext = filename_parts[-1]
    reader_func = SUPPORTED_FILETYPE_READERS.get(file_ext, None)
    # If reader_func is None, we don't yet support using the given file type.
    if not reader_func:
        supported_types_list = [
            filetype for filetype in SUPPORTED_FILETYPE_READERS.keys()
        ]
        supported_types = "\n".join(supported_types_list)
        raise Exception(
            f"Unsupported file extension type. Try one of: \n{supported_types}"
        )
    return reader_func(filename)


def check_required_headings_exist(dataframe):
    """
    Check that a DataFrame has all the required headings that we need.

    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        A DataFrame to check for required headings.

    Raises
    ------
    Exception
        If a required field from the REQUIRED_FIELDS global list is not present
        in the DataFrame, and exception is raised.

    """
    df_columns = dataframe.columns
    for field in REQUIRED_FIELDS:
        if field not in df_columns:
            raise Exception(f"'{field}' required field doesn't exist in spreadsheet.")


def lowercase_column_headings(dataframe):
    """
    Create a lowercase column for every column in the DataFrame.

    We do this so we can keep our column accessing consistent. Note that this
    will create a copy of every column that isn't already lowercased.

    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        A DataFrame that we need to generate lowercased-heading columns for.

    """
    for column_name in dataframe.columns:
        dataframe[column_name.lower()] = dataframe[column_name]


def convert_to_json(row):
    """
    Convert a row from a DataFrame into a json payload.

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

    Parameters
    ----------
    row : pandas.core.series.Series
        A Series created from a row of data from the overall DataFrame.
        This can just be thought of as a row from the DataFrame, and is
        automatically passed into this function with the DataFrame.apply()
        function.

    """
    # Get the required fields.
    # These fields must exist, and have been checked before coming to this function.
    subject = str(row["subject"])
    email_body = str(row["body"])
    body_html = ""
    body_plain = ""
    content_type = ""
    if is_html(email_body):
        body_html = email_body
        content_type = 'text/html; charset="utf-8"'
    else:
        body_plain = email_body
        content_type = 'text/plain; charset="utf-8"'

    # Inboxagent current forces us to have angle brackets on the id
    # Strip them away if they are there, so it is safe to add them back.
    unique_id = str(row["unique_id"]).lstrip("<").rstrip(">")
    unique_id = f"<{unique_id}>"

    sent_date = (
        str(row["date"].isoformat()) if type(row["date"]) is not str else row["date"]
    )

    # Not required fields. These can be defaulted to something else if they don't exist.
    try:
        to_addr = str(row["to"])
    except KeyError:
        to_addr = "analysis@aportio-insights.com"

    try:
        from_addr = str(row["from"])
    except KeyError:
        from_addr = "client@aportio-insights.com"

    try:
        cc = str(row["cc"])
    except KeyError:
        cc = ""

    # look for multiple addresses in the columns
    cc_list = []
    for sep in [",", ";"]:
        if sep in to_addr:
            cc_list = to_addr.split(sep)
            to_addr = cc_list.pop(0)
            break
    to_addr = validate_email(to_addr)

    for sep in [",", ";"]:
        if sep in from_addr:
            from_addr = from_addr.split(sep).pop(0)
            break
    from_addr = validate_email(from_addr)

    for sep in [",", ";"]:
        if sep in cc:
            cc_list.extend(cc.split(sep))
            break
    cc_list = [validate_email(e) for e in cc_list]

    # Build the json body.
    json_body = {
        "headers": {
            "from": from_addr,
            "sender": from_addr,
            "date": sent_date,
            "to": to_addr,
            "message_id": unique_id,
            "subject": subject,
            "content_type": content_type,
        },
        "envelope": {},
        "plain": body_plain,
        "html": body_html,
        "attachments": [],
    }
    if cc_list:
        json_body["headers"]["cc"] = ",".join(cc_list)

    email_list.append(json_body)


def import_spreadsheet(file_name: str) -> list:
    """
    Import emails from a spreadsheet.
    """

    # Load the data into a pandas DataFrame
    df = read_spreadsheet_emails(file_name)

    # First, we should go through and convert all column headings to lowercase.
    # Note that this will copy the column with all its data and add it to the
    # DataFrame again, but with a lowercase version of the column name.
    lowercase_column_headings(df)

    # Check that all required fields exist in the DataFrame.
    check_required_headings_exist(df)

    # Use the DataFrame.apply() method to do something with each row in the DataFrame.
    # The passed-in function acts like a callback.
    df.apply(convert_to_json, axis=1)

    return email_list
