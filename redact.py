# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Tool to redact emails in JSON format and output to directory
"""

from vendor.scrub import Scrub

STREET_SUFFIXES = [
    "Street",
    "St",
    "Lane",
    "Ln",
    "Avenue",
    "Ave",
    "Av",
    "Road",
    "Rd",
    "Drive",
    "Dr",
    "Terrace",
    "Tce",
    "Place",
    "PlCrescent",
    "Cres",
    "Highway",
    "Hwy",
    "Parade",
    "Pde",
    "Close",
    "Cl",
    "Way",
    "Square",
    "Sq",
    "Quay",
    "Boulevard",
    "Blvd",
    "Esplanade",
    "Esp",
    "Track",
    "Trk",
    "Rise",
    "Loop",
    "Grove",
    "Gr",
    "Court",
    "Ct",
    "Loop",
    "Parkway",
    "Pkwy",
    "Circle",
    "Cir",
]


class PIIScrub(Scrub):
    def __init__(self):
        super().__init__()
        self.patterns = [
            ("bank_iban", r"\b([A-Z]{2}\d{2}[-\s]{0,1}[A-Z0-9-\s]{1,33}\d)\b"),
            ("nz_bank", r"\b\d{2}-\d{4}-\d{7}-\d{2,3}\b"),
            ("date", r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"),
            (
                "street",
                rf"(?i)\b\d{{1,}}\s{{0,}}[\w\s]+?\s{{1,}}({'|'.join(STREET_SUFFIXES)})\b",
            ),
            (
                "phone",
                r"(?<![-\d])(?:\+?(61|64))?\s?(?:\((?=.*\)))?(0?\d{1,3})\)?\s?(\d\d(?:[-\s](?=\d{3})|(?!\d\d[-\s]?\d[-\s]))\d\d[-\s]?\d[-\s]?\d{3}|\d{3,4}\s?\d{3,4})(?![-\d])",
            ),
            ("vehicle_rego", r"\b[A-Z]\d{2}[-\s][A-Z]{3,4}\b"),
            ("vehicle_rego", r"\b\d{3}[-\s]\d{3,4}\b"),
            ("vehicle_rego", r"\b\d[A-Z][\d]{4}[A-Z]\b"),
            ("vehicle_rego", r"\b\d[A-Z][\d]{5}\b"),
            ("vehicle_rego", r"\b\d[-\s][A-Z0-9]{5,6}\b"),
            ("vehicle_rego", r"\b[A-Z]{2,3}[-\s]?[A-Z0-9]{3}\b"),
            ("vehicle_rego", r"\b\d{3}[A-Z]\d{3}\b"),
            ("vehicle_rego", r"\b\d{0,1}\s{0,1}[A-Z]{2,4}[-\s]?[A-Z]{0,1}\d{2,4}\b"),
            ("vehicle_rego", r"\b\d{2,4}[-\s]?[A-Z]{1,4}\b"),
            ("vehicle_rego", r"\b[A-Z]{1,2}[-\s]?\d{5,6}\b"),
            ("vehicle_rego", r"\b\d{3,7}\b"),
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
