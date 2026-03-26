"""Command-line entry point for the CSV converter application.

This module exposes the main CLI command used to convert supported tabular
data files into sanitized output files suitable for CSV-based workflows.
"""

import click, logging
from pathlib import Path

from csv_converter.core import DatafileConverter

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s'
)


@click.command()
@click.argument('file', type=click.Path(path_type=Path), metavar="<file>")
@click.option('--output', '-o', type=click.Path(path_type=Path), help='File destination .csv')
def main(file: Path, output:Path | None) -> None:
    """Convert data files to CSV.

    Converts tabular data files (XLSX, XLS, ODS) to CSV.
    Normalizes columns with conflicting data to allow safe conversion.

    Args:

        file: Path to the input file to be converted.

        output: Optional destination path for the generated CSV file.

    Returns:

        None: This function does not return a value.
    """
    try:
        converter = DatafileConverter(file, output)
        converter.process()
    except (FileNotFoundError, ValueError) as error:
        raise click.ClickException(f'{error}')

if __name__ == '__main__':
    main()
