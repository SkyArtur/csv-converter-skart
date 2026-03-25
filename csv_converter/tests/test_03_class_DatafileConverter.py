"""Tests for the ``DatafileConverter`` conversion workflow."""

import pytest, logging, shutil
from pathlib import Path
from csv_converter.core import DatafileConverter


def test_raised_exception_not_zipped_file(error_file: Path, caplog):
    """Validate logging and failure for a non-zip XLSX input.

    Args:
        error_file: Invalid XLSX file that cannot be treated as a zip archive.
        caplog: Pytest fixture used to capture emitted log messages.
    """
    with pytest.raises(ValueError):
        converter = DatafileConverter(error_file)
        with caplog.at_level(logging.ERROR):
            converter.process()
    assert 'File is not a zip file' in caplog.text
    shutil.rmtree(f'FileErrorNormalized')

def test_raised_exception_invalid_output_file(original_excel: Path, error_file: Path, caplog):
    """Validate logging and failure for an invalid output extension.

    Args:
        original_excel: Valid XLSX file used as input.
        error_file: Output path with an unsupported extension.
        caplog: Pytest fixture used to capture emitted log messages.
    """
    with pytest.raises(ValueError):
        converter = DatafileConverter(original_excel, error_file)
        with caplog.at_level(logging.ERROR):
            converter.process()
    assert 'Invalid output file extension - ".xlsx"' in caplog.text

def test_raised_exception_when_an(not_file, caplog):
    """Validate logging and failure for a missing input file.

    Args:
        not_file: Path that does not point to a valid file.
        caplog: Pytest fixture used to capture emitted log messages.
    """
    with pytest.raises(ValueError):
        datafile = DatafileConverter(not_file)
        with caplog.at_level(logging.ERROR):
            datafile.process()
    assert f'Parameter [ {not_file.name} ] not a file.' in caplog.text

def test_generate_file_csv_without_output(original_excel, debug_output_csv, root_tests):
    """Validate CSV generation in the default output directory.

    Args:
        original_excel: Valid XLSX file used as input.
        debug_output_csv: Fixture that exposes a debug CSV path.
        root_tests: Root path of the test package.
    """
    path_output = root_tests.joinpath('FileOriginalNormalized')
    converter = DatafileConverter(original_excel)
    converter.process()
    assert path_output.exists() == True
    assert path_output.joinpath('original.csv').exists() == True
    shutil.rmtree('FileOriginalNormalized')

def test_generate_file_csv_with(original_excel, debug_output_csv):
    """Validate CSV generation at an explicit output path.

    Args:
        original_excel: Valid XLSX file used as input.
        debug_output_csv: Explicit output path expected after processing.
    """
    converter = DatafileConverter(original_excel, debug_output_csv)
    converter.process()
    assert debug_output_csv.exists() == True
    debug_output_csv.unlink()
