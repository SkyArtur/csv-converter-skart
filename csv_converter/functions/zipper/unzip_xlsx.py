"""Helpers for extracting XLSX files into temporary directories."""

import zipfile
from pathlib import Path

from csv_converter.functions.decorator import exception_handling


@exception_handling
def unzip_xlsx(file: Path, temp_dir: Path) -> None:
    """Extract an XLSX file into a temporary directory.

    Args:
        file: Source XLSX file to extract.
        temp_dir: Destination directory for the extracted contents.

    Raises:
        FileNotFoundError: If ``file`` does not exist or is not a file.
        ValueError: If the archive cannot be opened by the wrapped decorator.
    """
    if not file.exists() or not file.is_file():
        raise FileNotFoundError(f':func: {unzip_xlsx.__name__} >> File "{file.name}" not found.')
    with zipfile.ZipFile(file) as zip_ref:
        zip_ref.extractall(temp_dir)
    return None
