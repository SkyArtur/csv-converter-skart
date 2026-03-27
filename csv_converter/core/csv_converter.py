import logging
from pathlib import Path
from typing import Optional

from .datafile_converter import DatafileConverter

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s'
)


logger = logging.getLogger(__name__)


def csv_converter(file: Path , output: Path | None = None) -> Optional[Path]:
    """Convert a supported file to CSV and return the output path.

    Args:
        file: Source file to convert.
        output: Optional target path for the generated CSV file.

    Returns:
        Optional[Path]: Generated CSV path when conversion succeeds; otherwise,
            ``None``.
    """
    try:
        converter = DatafileConverter(file, output, disable_cli=True)
        converter.process()
        return converter.output
    except Exception as e:
        func = csv_converter.__name__.title().replace('_', '-').upper()
        class_err = e.__class__.__name__
        logger.error(f'{func}[ {class_err} ] {e}.')
