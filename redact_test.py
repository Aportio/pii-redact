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
    test_data = {  # text, expected_text
        (
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd>",
            "http://[[REDACTED]]/TR/xhtml1/DTD/[[REDACTED]]>",
        ),
        (
            'xmlns="http://www.w3.org/1999/xhtml" ',
            'xmlns="http://[[REDACTED]]/[REDACTED]/xhtml" ',
        ),
    }
    for text, expected_text in test_data:
        scrubbed_text_from_tool = scrubber.scrub_text(text)

        assert scrubbed_text_from_tool == expected_text
