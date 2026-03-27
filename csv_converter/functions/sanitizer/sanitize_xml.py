"""Helpers for sanitizing spreadsheet XML content."""

import re


def sanitize_xml(xml: str) -> str:
    """Sanitize spreadsheet XML content.

    Args:
        xml: Raw XML content to sanitize.

    Returns:
        str: Sanitized XML content with placeholder numeric values, escaped
            ampersands, and invalid control characters removed.

    Raises:
        TypeError: If ``xml`` is not a string value accepted by ``re.sub()``.
    """
    xml = re.sub(r"(<(?:\w+:)?[vt]>)\s*-\s*(</(?:\w+:)?[vt]>)", r"\g<1>0\g<2>", xml)
    xml = re.sub(r"&(?!(amp|lt|gt|quot|apos);)", "&amp;", xml)
    xml = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", xml)
    return xml
