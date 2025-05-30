# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Tool to redact emails in JSON format and output to directory
"""

from vendor.scrub import Scrub


class PIIScrub(Scrub):
    def __init__(self):
        super().__init__()
        self.patterns = [
            ("bank_iban", r"\b([A-Z]{2}\d{2}[-\s]{0,1}[A-Z0-9-\s]{1,33}\d)\b"),
            ("nz_bank", r"\b\d{2}-\d{4}-\d{7}-\d{2,3}\b"),
            (
                "street",
                r"(?i)\b\d{1,}\s{0,}[\w\s]+?\s{1,}(Street|St|Lane|Ln|Avenue|Ave|Av|Road|Rd)\b",
            ),
            (
                "phone",
                r"(?<![-\d])(?:\+?(61|64))?\s?(?:\((?=.*\)))?(0?\d{1,3})\)?\s?(\d\d(?:[-\s](?=\d{3})|(?!\d\d[-\s]?\d[-\s]))\d\d[-\s]?\d[-\s]?\d{3}|\d{3,4}\s?\d{3,4})(?![-\d])",
            ),
            ("vehicle_rego", r"\b\d{0,1}\s{0,1}[A-Z]{2,4}[-\s]?[A-Z]{0,1}\d{2,4}\b"),
            ("vehicle_rego", r"\b\d{2,4}[-\s]?[A-Z]{2,4}\b"),
            ("vehicle_rego", r"\b[A-Z]{2}[-\s]?\d{5}\b"),
            (
                "url",
                r"\b((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
            ),
            *self.patterns,
        ]


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
