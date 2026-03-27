"""Tests for the ``DatafileConverter`` conversion workflow."""

import pytest, logging, shutil, click, zipfile
from click.testing import CliRunner
from pathlib import Path
from csv_converter.core import DatafileConverter


def test_raised_exception_not_zipped_file(error_file: Path, default_output_error, caplog):
    """Verify failure and logging for an invalid XLSX input.

    Args:
        error_file: Invalid XLSX file that cannot be treated as a zip archive.
        default_output_error: Default output directory derived from the invalid
            XLSX fixture.
        caplog: Pytest fixture used to capture emitted log messages.

    Raises:
        AssertionError: If the converter does not raise the expected error,
            does not log the expected message, or does not create the output
            directory.
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(zipfile.BadZipFile):
            DatafileConverter(error_file).process()
    assert 'File is not a zip file' in caplog.text
    assert 'BadZipFile' in caplog.text
    assert default_output_error.exists() == True
    shutil.rmtree(default_output_error)

def test_raised_exception_invalid_output_file(original_excel: Path, error_file: Path, caplog):
    """Verify failure and logging for an invalid output extension.

    Args:
        original_excel: Valid XLSX file used as input.
        error_file: Output path with an unsupported extension.
        caplog: Pytest fixture used to capture emitted log messages.

    Raises:
        AssertionError: If the converter does not reject the output path or
            does not log the expected message.
    """
    with caplog.at_level(logging.INFO):
        with pytest.raises(ValueError):
            DatafileConverter(original_excel, error_file).process()
    assert 'Invalid output file extension ".xlsx"' in caplog.text

def test_raised_exception_when_an(not_file, caplog):
    """Verify failure and logging for an invalid input path.

    Args:
        not_file: Path that does not point to a valid file.
        caplog: Pytest fixture used to capture emitted log messages.

    Raises:
        AssertionError: If the converter does not raise the expected error or
            does not log the expected message.
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            DatafileConverter(not_file).process()
    assert 'Not a valid file name' in caplog.text

def test_generate_file_csv_without_output_file(original_excel, default_output_dir):
    """Verify CSV generation in the default output directory.

    Args:
        original_excel: Valid XLSX file used as input.
        default_output_dir: Default output directory derived from the input
            fixture.

    Raises:
        AssertionError: If the converter does not create the expected output
            directory or CSV file.
    """
    converter = DatafileConverter(original_excel)
    converter.process()
    assert converter.output.exists() == True
    assert converter.output.parent == default_output_dir
    assert converter.output.name == f'{original_excel.stem}.csv'
    shutil.rmtree(default_output_dir)

def test_generate_file_csv_with_output_file(original_excel, debug_output_csv):
    """Verify CSV generation at an explicit output path.

    Args:
        original_excel: Valid XLSX file used as input.
        debug_output_csv: Explicit output path expected after processing.

    Raises:
        AssertionError: If the converter does not create the CSV file at the
            requested location.
    """
    converter = DatafileConverter(original_excel, debug_output_csv)
    converter.process()
    assert converter.output.exists() == True
    assert converter.output == debug_output_csv
    debug_output_csv.unlink()

@pytest.mark.parametrize("user_input, expected_exit_code", [
    pytest.param('y\n', 0, id='user_confirms'),
    pytest.param('n\n', 1, id='user_aborts')
])
def test_normalize_file_csv(original_csv, debug_output_csv, user_input, expected_exit_code):
    """Verify CSV normalization with interactive confidence prompts.

    Args:
        original_csv: CSV fixture used as converter input.
        debug_output_csv: Explicit output path expected after processing.
        user_input: Simulated terminal response passed to the Click command.
        expected_exit_code: Expected command exit code for the given input.

    Raises:
        AssertionError: If the command exit code or output file state does not
            match the expected result.
    """
    runner = CliRunner()
    @click.command()
    def run_converter():
        converter = DatafileConverter(original_csv, debug_output_csv)
        converter.process()
    result = runner.invoke(run_converter, input=user_input)
    assert result.exit_code == expected_exit_code
    if expected_exit_code == 0:
        assert debug_output_csv.exists() == True
        debug_output_csv.unlink()
    else:
        assert debug_output_csv.exists() == False
