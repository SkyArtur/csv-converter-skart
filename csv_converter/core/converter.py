"""Conversion workflow for supported spreadsheet and CSV inputs."""

import logging, pandas as pd
from pathlib import Path
from .filer import MainFiler
from csv_converter.functions import unzip_xlsx, zip_xlsx, sanitize_spreadsheets

logger = logging.getLogger(__name__)


class DatafileConverter:
    """Convert supported input files into normalized CSV output."""

    def __init__(self, file: Path, output: Path | None = None):
        """Initialize the converter with input and optional output paths.

        Args:
            file: Source file to convert.
            output: Optional destination path for the generated CSV file.
        """
        self.__file = file
        self.__output = output

    @staticmethod
    def save_new_file_csv(temp_file: Path, output: Path):
        """Persist a temporary spreadsheet as a CSV file.

        Args:
            temp_file: Temporary spreadsheet file generated during processing.
            output: Destination path for the resulting CSV file.
        """
        df = pd.read_excel(temp_file, engine='openpyxl')
        df.to_csv(output, index=False)

    @staticmethod
    def save_new_normalized_csv(file: Path, output: Path):
        """Persist a normalized UTF-8 copy of a CSV file.

        Args:
            file: Source CSV file to normalize.
            output: Destination path for the normalized CSV file.
        """
        df = pd.read_csv(file)
        df.to_csv(output, index=False, encoding='utf-8')

    def process(self):
        """Process the input file and generate CSV output.

        The workflow validates the source and destination paths, detects the
        input format, and applies the appropriate conversion path for CSV and
        Excel files.

        Raises:
            ValueError: If the input file format is not supported.
            Exception: Re-raises any exception produced during processing
                after logging it.
        """
        try:
            logger.info(f'Convertendo [ {self.__file.name} ] em CSV')
            with MainFiler(file=self.__file, output=self.__output) as filer:
                filer.validate_input_file()
                filer.validate_output_file()
                type_file = filer.detect_file_format()
                if type_file == 'csv':
                    self.save_new_normalized_csv(filer.file, filer.output)
                elif type_file == 'excel':
                    unzip_xlsx(filer.file, filer.temp_dir)
                    sanitize_spreadsheets(filer.temp_dir)
                    zip_xlsx(filer.temp_dir, filer.temp_file)
                    self.save_new_file_csv(filer.temp_file, filer.output)
                else:
                    logger.error(f"Formato não suportado: {filer.file.suffix}")
                    raise ValueError("Type file not supported.")
                logger.info(f'Arquivo [ {filer.output.name} ] gerado em: {filer.output.parent.resolve()}')
            return None
        except Exception as e:
            logger.error(e)
            raise
