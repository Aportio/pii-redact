## This is the scrub.py file from https://github.com/kylemclaren/scrub

import json
import re

import spacy

SPACY_LANGUAGE_MODEL = "en_core_web_lg"

# Load Spacy NLP model
try:
    nlp = spacy.load(SPACY_LANGUAGE_MODEL)
except OSError:
    print(f"Downloading spacy language model'{SPACY_LANGUAGE_MODEL}'")

    from spacy.cli import download

    download(SPACY_LANGUAGE_MODEL)
    nlp = spacy.load(SPACY_LANGUAGE_MODEL)


class Scrub:
    REDACT_ENTIES = ["PERSON", "DATE", "LOC", "FAC", "ORG", "GPE"]

    REDACTION_TEXT = "[REDACTED]"

    def __init__(self):
        self.patterns = [
            ("email", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            ("phone", r"\b\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}\b"),
            ("ssn", r"\b\d{3}[-]?\d{2}[-]?\d{4}\b"),
            (
                "ip_address_v4",
                r"\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b",
            ),
            ("ip_address_v6", r"\b(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}\b"),
            (
                "hostname",
                r"\b(?:(?:[a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*((?:[A-Za-z]|(?:[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9]))\.(?:[a-zA-Z]{2,})|(?:xn--[A-Za-z0-9]+))\b",
            ),
            (
                "uuid",
                r"\b(?:[0-9a-fA-F]){8}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){12}\b",
            ),
        ]

    def scrub_text(self, text: str) -> str:
        scrubbed_text = text
        for category, pattern in self.patterns:
            if category == "phone":
                matches = re.finditer(pattern, scrubbed_text)
                for match in matches:
                    matched_phone = match.group(0)

                    # Remove parentheses from matched phone numbers
                    matched_phone = re.sub(r"^\((\d{3})\)$", r"\1", matched_phone)
                    scrubbed_text = scrubbed_text.replace(matched_phone, self.REDACTION_TEXT)
            else:
                scrubbed_text = re.sub(pattern, self.REDACTION_TEXT, scrubbed_text)

        scrubbed_text = self.scrub_pii_with_nlp(scrubbed_text)
        return scrubbed_text

    def scrub_pii_with_nlp(self, text: str) -> str:
        nlp_doc = nlp(text)
        final_text = text

        for name in nlp_doc.ents:
            if name.label_ in self.REDACT_ENTIES:
                final_text = re.sub(re.escape(name.text), self.REDACTION_TEXT, final_text)
        return final_text

    def scrub(self, input_data: str | dict, original_format: str = "txt") -> str | dict:
        if original_format == "json":
            scrubbed_data = json.loads(input_data)
            scrubbed_data = self.scrub_dict(scrubbed_data)
        elif original_format == "ndjson":
            scrubbed_data = [
                self.scrub_dict(json.loads(line)) for line in input_data.splitlines()
            ]
        else:
            scrubbed_data = self.scrub_text(input_data)
        return scrubbed_data

    def scrub_dict(self, data: dict) -> dict:
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self.scrub_dict(value)
            elif isinstance(value, list):
                data[key] = [
                    self.scrub_dict(item) if isinstance(item, dict) else item for item in value
                ]
            elif isinstance(value, str):
                data[key] = self.scrub_text(value)
        return data
