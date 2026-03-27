"""Helpers for detecting file text encoding."""

import chardet
from pathlib import Path


def detect_encoding(file: Path) -> dict[str, str]:
    """Detect the most likely text encoding for a file.

    Args:
        file: File path whose raw bytes will be analyzed.

    Returns:
        dict[str, str]: Mapping returned by ``chardet.detect()`` with the
            detected encoding metadata.

    Raises:
        FileNotFoundError: If ``file`` does not exist.
        PermissionError: If the file cannot be opened for reading.
    """
    with open(file, 'rb') as csv_file:
        content = csv_file.read()
        detected = chardet.detect(content)
    return dict(detected)
