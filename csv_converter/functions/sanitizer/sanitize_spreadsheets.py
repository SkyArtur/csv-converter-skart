"""Helpers for sanitizing spreadsheet XML files within a directory tree."""
from pathlib import Path

from .sanitize_xml import sanitize_xml


def sanitize_spreadsheets(temp_dir: Path) -> Path:
    """Sanitize all spreadsheet XML files found under a directory.

    Args:
        temp_dir: Directory containing spreadsheet XML files to sanitize.

    Returns:
        Path: The same directory path received after sanitization completes.
    """
    for xml_file in temp_dir.glob('**/*.xml'):
        with xml_file.open('r', encoding='utf-8') as file_xml:
            xml = file_xml.read()
        xml = sanitize_xml(xml)
        with xml_file.open('w', encoding='utf-8') as file_xml:
            file_xml.write(xml)
    return temp_dir
