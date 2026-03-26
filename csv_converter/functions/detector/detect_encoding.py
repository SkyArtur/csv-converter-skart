"""Functions for detecting the text encoding of CSV-like files."""

import chardet
from pathlib import Path


def detect_encoding(file: Path) -> dict[str, str]:
    """Detect the most likely encoding for a file.

    Args:
        file: File whose raw bytes will be analyzed.

    Returns:
        dict[str, str]: Detection metadata returned by ``chardet``, including
        the encoding name and confidence value.

    Raises:
        FileNotFoundError: If ``file`` does not exist.
        PermissionError: If the file cannot be opened for reading.
    """
    with open(file, 'rb') as csv_file:
        content = csv_file.read()
        detected = chardet.detect(content)
    return dict(detected)
