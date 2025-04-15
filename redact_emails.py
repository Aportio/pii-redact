# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Tool to redact emails in JSON format and output to directory
"""

from scrubadubdub import Scrub


class PIIScrub(Scrub):
    def __init__(self):
        super().__init__()
        self.patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}\b",
            "phone1": r"(?:\+?(61|64))?\s?(?:\((?=.*\)))?(0?\d{1,3})\)?\s?(\d\d(?:[-\s]"
            r"(?=\d{3})|(?!\d\d[-\s]?\d[-\s]))\d\d[-\s]?\d[-\s]?\d{3}|\d{3,4}"
            r"\s?\d{3,4})",
            "ssn": r"\b\d{3}[-]?\d{2}[-]?\d{4}\b",
            "ip_address_v4": r"\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}"
            r"(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b",
            "ip_address_v6": r"\b(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}\b",
            "hostname": r"\b(?:(?:[a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*((?:[A-Za-z]|"
            r"(?:[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9]))\.(?:[a-zA-Z]{2,})|"
            r"(?:xn--[A-Za-z0-9]+))\b",
            "uuid": r"\b(?:[0-9a-fA-F]){8}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){4}-"
            r"(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){12}\b",
        }


def redact_text(text: str) -> str:
    """
    Redact the personal identifiable information from a given text.

    In case of any error, return empty text
    """
    try:
        scrubber = PIIScrub()
        scrubbed_text = scrubber.scrub(text)
        return scrubbed_text
    except BaseException as e:
        print(f"Exception occured : {e}")
        return ""
