"""Helpers for extracting XLSX archives into temporary directories."""

import zipfile
from pathlib import Path

from .zippers_decorator import zippers_decorator


@zippers_decorator
def unzip_xlsx(file: Path, temp_dir: Path) -> None:
    """Extract an XLSX archive into a temporary directory.

    Args:
        file: Source XLSX file to extract.
        temp_dir: Destination directory for the extracted contents.

    Raises:
        FileNotFoundError: If ``file`` does not exist or is not a file.
    """
    if not file.exists() or not file.is_file():
        raise FileNotFoundError(f'File [ {file.name} ] not found.')
    with zipfile.ZipFile(file) as zip_ref:
        zip_ref.extractall(temp_dir)
    return None
