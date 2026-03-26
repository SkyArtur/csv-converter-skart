"""Conversion services for normalizing spreadsheet and CSV inputs to CSV."""

import logging, click, pandas as pd
from pathlib import Path
from .filer import MainFiler
from csv_converter.functions import (
    unzip_xlsx,
    zip_xlsx,
    sanitize_spreadsheets,
    verify_confidence,
    detect_encoding
)

logger = logging.getLogger(__name__)


class DatafileConverter:
    """Convert supported files into normalized CSV output."""

    def __init__(self, file: Path, output: Path | None = None):
        """Initialize the converter with input and optional output paths.

        Args:
            file: Source file to convert.
            output: Optional destination path for the generated CSV file.
        """
        self.__file = file
        self.__output = output

    @staticmethod
    def check_confidence_csv(detection: dict[str, str], filer: MainFiler) -> str:
        """Validate encoding detection confidence before processing a CSV file.

        Args:
            detection: Raw encoding detection result.
            filer: File manager that stores the source file metadata.

        Returns:
            str: Encoding selected for CSV reading.

        Raises:
            ValueError: If the confidence tag cannot be mapped to a supported
                action.
            click.Abort: If the confidence is low and the user declines to
                continue.
        """
        verification = verify_confidence(detection)
        match verification['tag']:
            case 'high':
                logger.info(f'Confiabilidade [ {verification['value']:.2%} ]: Convertendo arquivo {filer.file.name}.')
            case 'medium':
                logger.warning(f'Confiabilidade [ {verification['value']:.2%} ]: Tentando converter arquivo {filer.file.name}.')
            case 'low':
                click.confirm(f'Confiança baixa [{verification['value']:.2%}]. Deseja continuar? y/n', abort=True)
        return verification['encoding']

    @staticmethod
    def save_new_file_csv(temp_file: Path, output: Path):
        """Write an Excel file stored in a temporary path as a CSV file.

        Args:
            temp_file: Temporary spreadsheet file to read.
            output: Destination CSV path.

        Raises:
            FileNotFoundError: If ``temp_file`` does not exist.
            ValueError: If the spreadsheet content cannot be parsed by pandas.
        """
        df = pd.read_excel(temp_file, engine='openpyxl')
        df.to_csv(output, index=False)

    @staticmethod
    def save_new_normalized_csv(file: Path, output: Path, encoding: str = 'utf-8'):
        """Read a CSV file and rewrite it using UTF-8 encoding.

        Args:
            file: Source CSV file.
            output: Destination CSV path.
            encoding: Encoding used to read the source file.

        Raises:
            FileNotFoundError: If ``file`` does not exist.
            ValueError: If pandas cannot parse the CSV content.
        """
        df = pd.read_csv(file, encoding=encoding, sep=None, engine='python')
        df.to_csv(output, index=False, encoding='utf-8')

    def process(self):
        """Run the complete conversion workflow for the configured file.

        Returns:
            None: This method returns ``None`` after a successful conversion.

        Raises:
            FileNotFoundError: If the input file or temporary resources cannot
                be created or located.
            ValueError: If the file format is unsupported, the output path is
                invalid, or one of the wrapped helper functions fails.
            Exception: Re-raises any unexpected exception raised during the
                conversion flow.
        """
        try:
            logger.info(f'Convertendo [ {self.__file.name} ] em CSV')
            with MainFiler(file=self.__file, output=self.__output) as filer:
                filer.validate_input_file()
                filer.validate_output_file()
                type_file = filer.detect_suffix()
                if type_file == 'csv':
                    detection = detect_encoding(filer.file)
                    encoding = self.check_confidence_csv(detection, filer)
                    self.save_new_normalized_csv(filer.file, filer.output, encoding)
                elif type_file == 'xlsx':
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
