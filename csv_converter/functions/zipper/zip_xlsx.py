"""Helpers for packaging extracted spreadsheet contents as XLSX."""

import zipfile
from pathlib import Path

from csv_converter.functions.decorator import exception_handling


@exception_handling
def zip_xlsx(temp_dir: Path, temp_file: Path) -> None:
    """Compress a temporary directory into an XLSX-compatible archive.

    Args:
        temp_dir: Directory containing the extracted XLSX structure.
        temp_file: Target path for the generated archive file.

    Raises:
        FileNotFoundError: If ``temp_dir`` does not exist or is not a
            directory.
    """
    if not temp_dir.exists():
        raise FileNotFoundError(f':func: {zip_xlsx.__name__} >> Temporary directory "{temp_dir.name}" does not exist.')
    elif not temp_dir.is_dir():
        raise FileNotFoundError(f':func: {zip_xlsx.__name__} >> Directory "{temp_dir.name}" is not a directory.')
    with zipfile.ZipFile(temp_file, 'w') as new_zip:
        for file in temp_dir.rglob('*'):
            if file.is_file():
                new_zip.write(file, file.relative_to(temp_dir))
    return None

