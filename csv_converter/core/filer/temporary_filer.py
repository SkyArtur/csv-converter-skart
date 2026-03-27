"""Temporary workspace helpers for spreadsheet conversion."""

import shutil, tempfile, logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class TemporaryFiler:
    """Manage temporary resources used during spreadsheet processing."""

    def __init__(self, **kwargs):
        """Initialize temporary workspace attributes.

        Args:
            **kwargs: Extra keyword arguments forwarded to ``super()``.
        """
        super().__init__(**kwargs)
        self.__temporary_directory: Optional[Path] = None
        self.temp_dir: Optional[Path] = None
        self.temp_file: Optional[Path] = None
        self.temp_dir_xl: Optional[Path] = None

    def __enter__(self):
        """Create the temporary directory structure.

        Returns:
            TemporaryFiler: Current instance with initialized temporary paths.

        Raises:
            FileNotFoundError: If any required temporary path is not created.
        """
        self.__temporary_directory = Path(tempfile.mkdtemp()).resolve()
        self.temp_dir = self.__temporary_directory.joinpath('temp_spst').resolve()
        self.temp_dir_xl = self.temp_dir.joinpath('xl').resolve()
        self.temp_file = self.temp_dir.joinpath('temp.xlsx').resolve()
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir_xl.mkdir(parents=True, exist_ok=True)
        self.temp_file.touch(exist_ok=True)
        if not self.temp_dir.exists() or not self.temp_dir_xl.exists() or not self.temp_file.exists():
            raise FileNotFoundError(
                f':class: {self.__class__.__name__} >> Error defining the temporary file structure.'
            )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Remove temporary resources when leaving the context.

        Args:
            exc_type: Exception type raised inside the context, if any.
            exc_val: Exception instance raised inside the context, if any.
            exc_tb: Traceback raised inside the context, if any.

        Returns:
            bool: ``False`` to propagate exceptions.
        """
        shutil.rmtree(self.__temporary_directory, ignore_errors=True)
        return False
