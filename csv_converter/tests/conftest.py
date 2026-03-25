"""Shared pytest fixtures for filesystem-based converter tests."""

import tempfile, shutil, pytest
from typing import Generator
from pathlib import Path


@pytest.fixture
def root_tests() -> Path:
    return Path(__file__).parent

@pytest.fixture
def temporary_system_path():
    return Path(tempfile.gettempdir())

@pytest.fixture
def artifacts_dir(root_tests) -> Path:
    return root_tests / 'artifacts'

@pytest.fixture
def fixtures_dir(root_tests: Path) -> Path:
    return root_tests / 'fixtures'

@pytest.fixture
def debug_dir(artifacts_dir: Path) -> Path:
    return artifacts_dir / 'debug'

@pytest.fixture
def input_files_dir(fixtures_dir) -> Path:
    return fixtures_dir / 'input_files'

@pytest.fixture
def expected_files_dir(fixtures_dir) -> Path:
    return fixtures_dir / 'expected_files'

@pytest.fixture
def debug_temp_dir(debug_dir: Path) -> Generator[Path, None, None]:
    temp_dir = debug_dir / 'temp'
    if not temp_dir.exists():
        temp_dir.mkdir(exist_ok=True, parents=True)
    yield temp_dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        temp_dir.mkdir(exist_ok=True, parents=True)


@pytest.fixture
def debug_temp_file(debug_temp_dir: Path) -> Path:
    return debug_temp_dir / 'tmpfile.xlsx'

@pytest.fixture
def debug_output_csv(debug_dir) -> Path:
    return debug_dir / 'output.csv'

@pytest.fixture
def original_excel(input_files_dir: Path) -> Path:
    return input_files_dir / 'original.xlsx'

@pytest.fixture
def original_csv(input_files_dir: Path) -> Path:
    return input_files_dir / 'original.csv'

@pytest.fixture
def normalized_csv(expected_files_dir: Path) -> Path:
    return expected_files_dir / 'normalized.csv'

@pytest.fixture
def not_file(input_files_dir: Path) -> Path:
    return input_files_dir / 'not_file'

@pytest.fixture
def error_file(input_files_dir: Path) -> Path:
    return input_files_dir / 'error.xlsx'
