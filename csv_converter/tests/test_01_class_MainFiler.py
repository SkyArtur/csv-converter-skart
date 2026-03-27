"""Tests for the ``MainFiler`` filesystem orchestration behavior."""

import shutil, pytest
from pathlib import Path
from csv_converter.core import MainFiler


def test_invalid_input_file(not_file: Path) -> None:
    """Verify that ``validate_input_file()`` rejects an invalid file path.

    Args:
        not_file: Path that does not point to a valid file.
    """
    with MainFiler(not_file) as invalid_filer:
        with pytest.raises(ValueError):
            invalid_filer.validate_input_file()

def test_invalid_output_file(original_excel: Path, error_file: Path) -> None:
    """Verify that ``validate_output_file()`` rejects an invalid output path.

    Args:
        original_excel: Valid input spreadsheet used to build the filer.
        error_file: Output path with an unsupported extension.
    """
    with MainFiler(original_excel, error_file) as invalid_filer:
        with pytest.raises(ValueError) as e:
            invalid_filer.validate_output_file()

def test_creation_default_destination_directory(original_excel: Path) -> None:
    """Verify creation of the default output directory.

    Args:
        original_excel: Valid input spreadsheet used to build the filer.
    """
    with MainFiler(original_excel) as filer:
        filer.validate_output_file()
        assert filer.output.parent.exists() == True
        assert filer.output.parent.name == f'File{filer.file.stem.title()}Normalized'
        shutil.rmtree(filer.output.parent.name)

def test_define_temporary_structure(original_excel:Path, temporary_system_path: Path) -> None:
    """Verify the temporary directory structure created by ``MainFiler``.

    Args:
        original_excel: Valid input spreadsheet used to build the filer.
        temporary_system_path: Base temporary directory provided by the system.
    """
    with MainFiler(original_excel) as filer:
        assert filer.temp_dir.exists() == True
        assert filer.temp_dir.parent.parent == temporary_system_path
        assert filer.temp_dir_xl.exists() == True
        assert filer.temp_file.suffix == '.xlsx'
        assert filer.temp_file.is_relative_to(filer.temp_dir) == True
    assert filer.temp_dir.exists() == False
