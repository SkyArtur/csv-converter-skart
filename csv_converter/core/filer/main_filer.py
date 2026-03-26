"""File management helpers for validation and CSV output generation."""

import logging, pandas as pd
from typing import Optional
from pathlib import Path

from .temporary_filer import TemporaryFiler

logger = logging.getLogger(__name__)

class MainFiler(TemporaryFiler):
    """Manage source files, output paths, and temporary conversion state."""

    def __init__(self, file: Path , output: Optional[Path] = None, **kwargs):
        """Initialize the filer with input and optional output paths.

        Args:
            file: Source file to process.
            output: Optional destination path for the generated CSV file.
            **kwargs: Additional keyword arguments forwarded to the parent
                class.
        """
        super().__init__(**kwargs)
        self.file = file
        self.output = output

    def detect_suffix(self) -> Optional[str]:
        """Detect the supported format of the input file.

        Returns:
            Optional[str]: ``"excel"`` for Excel files, ``"csv"`` for CSV
            files, or ``None`` when the extension is unsupported.
        """
        suffix = self.file.suffix.lower()
        if suffix in ['.xlsx', '.xls']:
            return 'xlsx'
        if suffix in ['.csv', '.csv.gz']:
            return 'csv'
        return None

    def validate_input_file(self) -> Path:
        """Validate that the input path exists and points to a file.

        Returns:
            Path: Validated input file path.

        Raises:
            FileNotFoundError: If the input path does not exist.
            ValueError: If the input path is not a file.
        """
        if not self.file.exists():
            raise FileNotFoundError(f'<class: {self.__class__.__name__}> - File [ {self.file.name} ] not found.')
        if not self.file.is_file():
            raise ValueError(f'<class: {self.__class__.__name__}> - Parameter [ {self.file.name} ] not a file.')
        return self.file

    def validate_output_file(self) -> Path:
        """Validate or create the output path used for the generated CSV.

        Returns:
            Path: Resolved output CSV path.

        Raises:
            ValueError: If the provided output path does not use the ``.csv``
                extension.
            PermissionError: If the output directory cannot be created.
        """
        output_pattern = self.file.stem
        output_dir_pattern = Path.cwd().joinpath(f'File{output_pattern.title()}Normalized').resolve()
        if not self.output:
            output_dir_pattern.mkdir(parents=True, exist_ok=True)
            self.output = output_dir_pattern.joinpath(f'{output_pattern}.csv').resolve()
        else:
            if self.output.suffix != '.csv':
                raise ValueError(f'<class: {self.__class__.__name__}> - Invalid output file extension - "{self.output.suffix}"')
            if not self.output.parent.exists():
                self.output.parent.mkdir(parents=True, exist_ok=True)
        return self.output
