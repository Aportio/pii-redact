# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Test redact text
"""

import re

from redact import PIIScrub


def test_redact_urls():
    scrubber = PIIScrub()
    url_pattern = scrubber.patterns["url"]
    text = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"""
    scrubbed_text = re.sub(url_pattern, "[REDACTED]", text)
    scrubbed_text_from_tool = scrubber.scrub_text(text)

    print(scrubbed_text)

    print(scrubbed_text_from_tool)
    assert scrubbed_text == scrubbed_text_from_tool
