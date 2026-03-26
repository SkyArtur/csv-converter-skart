"""Tests for the ``DatafileConverter`` conversion workflow."""

import pytest, logging, shutil, click
from click.testing import CliRunner
from pathlib import Path
from csv_converter.core import DatafileConverter


def test_raised_exception_not_zipped_file(error_file: Path, default_output_error, caplog):
    """Validate logging and failure for a non-zip XLSX input.

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
        with pytest.raises(ValueError):
            DatafileConverter(error_file).process()
    assert default_output_error.exists() == True
    assert 'File is not a zip file' in caplog.text
    shutil.rmtree(default_output_error)

def test_raised_exception_invalid_output_file(original_excel: Path, error_file: Path, caplog):
    """Validate logging and failure for an invalid output extension.

    Args:
        original_excel: Valid XLSX file used as input.
        error_file: Output path with an unsupported extension.
        caplog: Pytest fixture used to capture emitted log messages.

    Raises:
        AssertionError: If the converter does not reject the output path or
            does not log the expected message.
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            DatafileConverter(original_excel, error_file).process()
    assert 'Invalid output file extension - ".xlsx"' in caplog.text

def test_raised_exception_when_an(not_file, caplog):
    """Validate logging and failure for a missing input file.

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
    assert f'Parameter [ {not_file.name} ] not a file.' in caplog.text

def test_generate_file_csv_without_output_file(original_excel, debug_output_csv, default_output_dir):
    """Validate CSV generation in the default output directory.

    Args:
        original_excel: Valid XLSX file used as input.
        debug_output_csv: Debug CSV path fixture kept for test composition.
        default_output_dir: Default output directory derived from the input
            fixture.

    Raises:
        AssertionError: If the converter does not create the expected output
            directory or CSV file.
    """
    converter = DatafileConverter(original_excel)
    converter.process()
    assert default_output_dir.exists() == True
    assert default_output_dir.joinpath(f'{original_excel.stem}.csv').exists() == True
    shutil.rmtree(default_output_dir)

def test_generate_file_csv_with_output_file(original_excel, debug_output_csv):
    """Validate CSV generation at an explicit output path.

    Args:
        original_excel: Valid XLSX file used as input.
        debug_output_csv: Explicit output path expected after processing.

    Raises:
        AssertionError: If the converter does not create the CSV file at the
            requested location.
    """
    converter = DatafileConverter(original_excel, debug_output_csv)
    converter.process()
    assert debug_output_csv.exists() == True
    debug_output_csv.unlink()

@pytest.mark.parametrize("user_input, expected_exit_code", [('y\n', 0), ('n\n', 1)])
def test_normalize_file_csv(original_csv, debug_output_csv, user_input, expected_exit_code):
    """Validate CSV normalization flow for interactive confidence prompts.

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
