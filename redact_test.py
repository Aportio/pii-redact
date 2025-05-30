# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Test redact text
"""

from redact import PIIScrub


def test_redact_urls():
    scrubber = PIIScrub()
    # text, expected_text
    test_data = [
        (
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd>",
            "http://[REDACTED]/TR/xhtml1/DTD/[REDACTED]>",
        ),
        (
            'xmlns="http://www.w3.org/1999/xhtml" ',
            '[REDACTED]" ',
        ),
    ]
    for test_num, (input_text, expected_text) in enumerate(test_data, start=1):
        scrubbed_text_from_tool = scrubber.scrub_text(input_text)

        assert scrubbed_text_from_tool == expected_text, f"#{test_num} failed"


def test_redact_text():
    scrubber = PIIScrub()
    # text, expected_text
    test_data = [
        (
            "John Smith, who was born 9th January, 2025, lives with David and Louise at the corner of East Street and 12th Ave.",
            "[REDACTED], who was born [REDACTED], lives with [REDACTED] and [REDACTED] at the corner of [REDACTED] and [REDACTED].",
        ),
        (
            "John Smith (9/01/2025), lives at 24 Walls St, London.",
            "[REDACTED] ([REDACTED]), lives at [REDACTED], [REDACTED].",
        ),
        (
            "John Smith (9/01/2025), lives at 24a Totara Avenue, Tauranga.",
            "[REDACTED] ([REDACTED]), lives at [REDACTED], [REDACTED].",
        ),
    ]
    for test_num, (input_text, expected_text) in enumerate(test_data, start=1):
        scrubbed_text_from_tool = scrubber.scrub_text(input_text)

        assert scrubbed_text_from_tool == expected_text, f"#{test_num} failed"
