"""Shared pytest fixtures for filesystem-based converter tests."""

import tempfile, shutil, pytest, pandas as pd
from typing import Generator
from pathlib import Path

from csv_converter.core import MainFiler
from csv_converter.functions import detect_encoding


@pytest.fixture
def root_tests() -> Path:
    """Return the root directory of the test package.

    Returns:
        Path: Absolute path to the test package directory.
    """
    return Path(__file__).parent

@pytest.fixture
def temporary_system_path():
    """Return the system temporary directory path.

    Returns:
        Path: System temporary directory path.
    """
    return Path(tempfile.gettempdir())

@pytest.fixture
def engines_csv():
    """Return the CSV parser engine names used by the tests.

    Returns:
        dict[str, str]: Mapping of engine names to themselves.
    """
    return {e: e for e in ['c', 'python', 'pyarrow', 'python-fwf']}

@pytest.fixture
def artifacts_dir(root_tests) -> Path:
    """Return the directory used for generated test artifacts.

    Args:
        root_tests: Root directory of the test package.

    Returns:
        Path: Directory used to store generated test artifacts.
    """
    return root_tests / 'artifacts'

@pytest.fixture
def fixtures_dir(root_tests: Path) -> Path:
    """Return the directory that stores static test fixtures.

    Args:
        root_tests: Root directory of the test package.

    Returns:
        Path: Directory that stores static test fixtures.
    """
    return root_tests / 'fixtures'

@pytest.fixture
def debug_dir(artifacts_dir: Path) -> Path:
    """Return the directory used for debug artifacts.

    Args:
        artifacts_dir: Root directory for generated test artifacts.

    Returns:
        Path: Directory used to store debug outputs.
    """
    return artifacts_dir / 'debug'

@pytest.fixture
def input_files_dir(fixtures_dir) -> Path:
    """Return the directory that stores input fixture files.

    Args:
        fixtures_dir: Root directory for static test fixtures.

    Returns:
        Path: Directory that stores input fixture files.
    """
    return fixtures_dir / 'input_files'

@pytest.fixture
def expected_files_dir(fixtures_dir) -> Path:
    """Return the directory that stores expected output fixtures.

    Args:
        fixtures_dir: Root directory for static test fixtures.

    Returns:
        Path: Directory that stores expected output fixture files.
    """
    return fixtures_dir / 'expected_files'

@pytest.fixture
def debug_temp_dir(debug_dir: Path) -> Generator[Path, None, None]:
    """Provide a reusable temporary directory for debug artifacts.

    Args:
        debug_dir: Directory used for debug artifacts.

    Yields:
        Path: Temporary directory created under the debug artifacts path.

    Raises:
        PermissionError: If the temporary directory cannot be created or
            removed.
    """
    temp_dir = debug_dir / 'temp'
    if not temp_dir.exists():
        temp_dir.mkdir(exist_ok=True, parents=True)
    yield temp_dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        temp_dir.mkdir(exist_ok=True, parents=True)

@pytest.fixture
def debug_temp_file(debug_temp_dir: Path) -> Path:
    """Return the temporary XLSX path used in debug tests.

    Args:
        debug_temp_dir: Temporary debug directory used by zipper tests.

    Returns:
        Path: Temporary XLSX file path.
    """
    return debug_temp_dir / 'tmpfile.xlsx'

@pytest.fixture
def debug_output_csv(debug_dir) -> Path:
    """Return the explicit CSV output path used in debug tests.

    Args:
        debug_dir: Directory used for debug artifacts.

    Returns:
        Path: Explicit CSV output path for debug-oriented tests.
    """
    return debug_dir / 'output.csv'

@pytest.fixture
def original_excel(input_files_dir: Path) -> Path:
    """Return the valid XLSX fixture path.

    Args:
        input_files_dir: Directory that stores input fixture files.

    Returns:
        Path: Valid XLSX input fixture path.
    """
    return input_files_dir / 'original.xlsx'

@pytest.fixture
def original_csv(input_files_dir: Path) -> Path:
    """Return the valid CSV fixture path.

    Args:
        input_files_dir: Directory that stores input fixture files.

    Returns:
        Path: Valid CSV input fixture path.
    """
    return input_files_dir / 'original.csv'

@pytest.fixture
def normalized_csv(expected_files_dir: Path) -> Path:
    """Return the expected normalized CSV fixture path.

    Args:
        expected_files_dir: Directory that stores expected output fixtures.

    Returns:
        Path: Expected normalized CSV fixture path.
    """
    return expected_files_dir / 'normalized.csv'

@pytest.fixture
def not_file(input_files_dir: Path) -> Path:
    """Return a path that is invalid as a file input.

    Args:
        input_files_dir: Directory that stores input fixture files.

    Returns:
        Path: Path that is expected to be invalid as a regular file input.
    """
    return input_files_dir

@pytest.fixture
def error_file(input_files_dir: Path) -> Path:
    """Return the invalid XLSX fixture used in error scenarios.

    Args:
        input_files_dir: Directory that stores input fixture files.

    Returns:
        Path: Invalid XLSX fixture path.
    """
    return input_files_dir / 'error.xlsx'

@pytest.fixture
def default_output_dir(original_excel: Path, root_tests: Path) -> Path:
    """Return the default output directory for the valid XLSX fixture.

    Args:
        original_excel: Valid XLSX fixture used to derive the default output.
        root_tests: Root directory of the test package.

    Returns:
        Path: Default output directory created for the valid XLSX fixture.
    """
    with MainFiler(original_excel) as filer:
        filer.validate_output_file()
        output_dir = filer.output.parent
    return output_dir

@pytest.fixture
def default_output_error(error_file: Path, root_tests: Path) -> Path:
    """Return the default output directory for the invalid XLSX fixture.

    Args:
        error_file: Invalid XLSX fixture used to derive the default output.
        root_tests: Root directory of the test package.

    Returns:
        Path: Default output directory created for the invalid XLSX fixture.
    """
    with MainFiler(error_file) as filer:
        filer.validate_output_file()
        output_dir = filer.output.parent
    return output_dir
