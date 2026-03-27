"""Tests for the public ``csv_converter()`` helper."""

import logging, shutil, pytest, zipfile
from csv_converter import csv_converter
from pathlib import Path



def test_raised_exception_not_zipped_file(error_file: Path, default_output_error, caplog):
    """Verify logging for an invalid XLSX input.

    Args:
        error_file: Invalid XLSX fixture passed to the public helper.
        default_output_error: Default output directory derived from the invalid
            fixture.
        caplog: Pytest fixture used to capture emitted log messages.
    """
    with caplog.at_level(logging.ERROR):
        csv_converter(error_file)
    assert 'File is not a zip file' in caplog.text
    assert 'BadZipFile' in caplog.text
    shutil.rmtree(default_output_error)

def test_raised_exception_invalid_output_file(original_excel: Path, error_file: Path, caplog):
    """Verify logging for an invalid output extension.

    Args:
        original_excel: Valid XLSX fixture used as input.
        error_file: Output path with an unsupported extension.
        caplog: Pytest fixture used to capture emitted log messages.
    """
    with caplog.at_level(logging.INFO):
        csv_converter(original_excel, error_file)
    assert 'Invalid output file extension ".xlsx"' in caplog.text

def test_raised_exception_invalid_file_name(not_file, caplog):
    """Verify logging for an invalid input path.

    Args:
        not_file: Path that is invalid as a regular file input.
        caplog: Pytest fixture used to capture emitted log messages.
    """
    with caplog.at_level(logging.ERROR):
        csv_converter(not_file)
    assert 'Not a valid file name' in caplog.text

def test_generate_file_csv_without_output_file(original_excel, debug_output_csv, default_output_dir):
    """Verify CSV generation in the default output directory.

    Args:
        original_excel: Valid XLSX fixture used as input.
        debug_output_csv: Debug CSV path fixture retained for test signature
            compatibility.
        default_output_dir: Default output directory derived from the input
            fixture.
    """
    csv_converter(original_excel)
    assert default_output_dir.exists() == True
    assert default_output_dir.joinpath(f'{original_excel.stem}.csv').exists() == True
    shutil.rmtree(default_output_dir)

def test_generate_file_csv_with_output_file(original_excel, debug_output_csv):
    """Verify CSV generation at an explicit output path.

    Args:
        original_excel: Valid XLSX fixture used as input.
        debug_output_csv: Explicit output path expected after conversion.
    """
    csv_converter(original_excel, debug_output_csv)
    assert debug_output_csv.exists() == True
    debug_output_csv.unlink()
