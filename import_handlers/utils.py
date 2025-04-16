# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Common utility functions.
"""

from email.utils import parseaddr


def lowercase_keys(dic, lkeys) -> None:
    """
    Modify passed-in dictionary by converting specified keys to lower-case.

    The conversion will work, no matter what mixed case was used in the original
    key.

    Other keys (any that aren't specified) are left as they are.

    """
    # Note: make list first, don't use generator directly since dict is modified
    for k in list(dic.keys()):
        lower_k = k.lower()
        if k == lower_k:
            # lower case already, can ignore
            continue
        if lower_k in lkeys and lower_k not in dic:
            dic[lower_k] = dic[k]
            del dic[k]


def is_html(email_body: str) -> bool:
    """
    Test the email for HTML tags.
    """
    return ("<html" in email_body and "</html" in email_body) or "text/html" in email_body


def validate_email(email_address: str) -> str:
    """
    Validate the email address.

    The Inboxagent code requires proper emails with domains and everything.
    """
    # Clean out illegal characters
    email_address = email_address.replace(" ", "")

    if not email_address:
        # Raise the exception since the caller is already handling this
        raise KeyError("Blank email address")

    _, email = parseaddr(email_address)
    if "@" not in email:
        name = email
        domain = "undefined.email"
    else:
        name, domain = email.split("@")
        if "." not in domain:
            domain += ".undefined"

    return f"{name}@{domain}"
