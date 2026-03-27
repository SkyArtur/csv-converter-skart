"""Tests for the XLSX zip and unzip helper functions."""

import pytest
from pathlib import Path
from csv_converter.core import MainFiler
from csv_converter.functions import zip_xlsx, unzip_xlsx


def test_unzip_xlsx(debug_temp_dir: Path, original_excel: Path) -> None:
    """Verify that ``unzip_xlsx()`` extracts an XLSX file into the target directory.

    Args:
        debug_temp_dir: Temporary directory used for extracted files.
        original_excel: Valid XLSX file used as extraction source.
    """
    temp_dir = debug_temp_dir
    file = original_excel
    unzip_xlsx(file, temp_dir)
    assert temp_dir.exists() == True
    assert temp_dir.joinpath('xl').exists() == True
    for file in temp_dir.glob('*.xml'):
        assert file.exists() == True

def test_zip_xlsx(debug_temp_dir: Path, debug_temp_file: Path) -> None:
    """Verify that ``zip_xlsx()`` creates an XLSX file from a directory.

    Args:
        debug_temp_dir: Directory used as compression source.
        debug_temp_file: Output file expected after compression.
    """
    temp_dir = debug_temp_dir
    temp_file = debug_temp_file
    zip_xlsx(temp_dir, temp_file)
    assert temp_file.exists() == True

def test_unzip_xlsx_extract_xml_structure(original_excel):
    """Verify that extracted XLSX content contains XML files.

    Args:
        original_excel: Valid XLSX file used as extraction source.
    """
    with MainFiler(original_excel) as filer:
        unzip_xlsx(filer.file, filer.temp_dir)
        for element in filer.temp_dir.rglob('*.xml'):
            assert element.exists()

def test_zip_xlsx_create_temporary_xlsx(original_excel):
    """Verify that ``zip_xlsx()`` creates the temporary XLSX path.

    Args:
        original_excel: Valid XLSX file used to build the filer structure.
    """
    with MainFiler(original_excel) as filer:
        zip_xlsx(filer.temp_dir, filer.temp_file)
        for element in filer.temp_dir.rglob('*.xlsx'):
            assert element.resolve() == filer.temp_file

def test_unzip_xlsx_raised_value_error_because_file_not_fund(not_file, error_file):
    """Verify that ``unzip_xlsx()`` rejects an invalid source path.

    Args:
        not_file: Path that does not point to a valid file.
        error_file: Path reused as the extraction target.
    """
    file = not_file
    temp_dir = error_file
    with pytest.raises(FileNotFoundError) as err:
        unzip_xlsx(file, temp_dir)

def test_zip_xlsx_raised_value_error_because_not_a_dir(error_file):
    """Verify that ``zip_xlsx()`` rejects a source path that is not a directory.

    Args:
        error_file: Path reused as both invalid source and output target.
    """
    temp_dir = error_file
    temp_file = error_file
    with pytest.raises(FileNotFoundError):
        zip_xlsx(temp_dir, temp_file)
