"""Helpers for sanitizing spreadsheet XML files in a directory tree."""
from pathlib import Path

from .sanitize_xml import sanitize_xml


def sanitize_spreadsheets(temp_dir: Path) -> Path:
    """Sanitize all XML files found under a directory.

    Args:
        temp_dir: Root directory containing extracted spreadsheet XML files.

    Returns:
        Path: The same directory path after sanitization completes.

    Raises:
        FileNotFoundError: If a matched XML file is removed before it is read.
        PermissionError: If an XML file cannot be read or rewritten.
        TypeError: If ``sanitize_xml()`` receives invalid content.
    """
    for xml_file in temp_dir.glob('**/*.xml'):
        with xml_file.open('r', encoding='utf-8') as file_xml:
            xml = file_xml.read()
        xml = sanitize_xml(xml)
        with xml_file.open('w', encoding='utf-8') as file_xml:
            file_xml.write(xml)
    return temp_dir
