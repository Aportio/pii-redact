# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Test redact text
"""

from pathlib import Path

from redact import PIIScrub


def test_redact_urls():
    scrubber = PIIScrub()
    # text, expected_text
    test_data = [
        (
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd",
            "[REDACTED]",
        ),
        (
            'xmlns="http://www.w3.org/1999/xhtml"',
            'xmlns="[REDACTED][REDACTED]/xhtml"',
        ),
    ]
    for test_num, (input_text, expected_text) in enumerate(test_data, start=1):
        clean_text = scrubber.scrub_text(input_text)

        assert clean_text == expected_text, f"#{test_num} failed"


def test_redact_text():
    scrubber = PIIScrub()
    # text, expected_text
    test_data = [
        (
            "John Smith, who was born 9th January, 2025, lives with David and Louise at the corner of East Street and 12th Ave.",
            "[REDACTED], who was born [REDACTED], [REDACTED], lives with [REDACTED] and [REDACTED] at the corner of [REDACTED] and [REDACTED].",
        ),
        (
            "John Smith (9/01/2025), lives at 24 Walls St, London.",
            "[REDACTED] ([REDACTED]), lives at [REDACTED], [REDACTED].",
        ),
        (
            "John Smith (9/01/2025), lives at 24a Totara Avenue, Tauranga.",
            "[REDACTED] ([REDACTED]), lives at [REDACTED], [REDACTED].",
        ),
        (
            "John Smith (9/01/2025), lives at 24a Totara Avenue, Tauranga. Previously at 24 Walls St, London.",
            "[REDACTED] ([REDACTED]), lives at [REDACTED], [REDACTED]. Previously at [REDACTED], [REDACTED].",
        ),
        (
            "My bank account is 12-1234-1234567-12",
            "My bank account is [REDACTED]",
        ),
        (
            "My bank account is 12-1234-1234567-123",
            "My bank account is [REDACTED]",
        ),
        (
            "My IBAN account is GB82 WEST 1234 5698 7654 32",
            "My [REDACTED] account is [REDACTED]",
        ),
        (
            "My IBAN account is IE64 IRCE 9205 0112 3456 78 or IE64IRCE92050112345678",
            "My [REDACTED] account is [REDACTED] or [REDACTED]",
        ),
        (
            "My IBAN account is BI13 20001 10001 00001234567 89 or BI1320001100010000123456789",
            "My [REDACTED] account is [REDACTED] or [REDACTED]",
        ),
        (
            "My IBAN account is DE89-37040-04405-3201300",
            "My [REDACTED] account is [REDACTED]",
        ),
    ]
    for test_num, (input_text, expected_text) in enumerate(test_data, start=1):
        scrubbed_text_from_tool = scrubber.scrub_text(input_text)

        assert scrubbed_text_from_tool == expected_text, f"#{test_num} failed"


def test_redact_license_plates():
    scrubber = PIIScrub()
    test_file = Path(__file__).parent / "test_data" / "license_plates.txt"
    with test_file.open("r") as fh:
        test_data = fh.readlines()

    for test_num, plate in enumerate(test_data, start=1):
        clean_text = scrubber.scrub_text(plate)
        assert clean_text.strip() == scrubber.REDACTION_TEXT, (
            f"#{test_num} failed for {plate=}"
        )
