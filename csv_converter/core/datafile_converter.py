"""Services for converting supported data files to CSV."""

import logging, click, pandas as pd
from typing import Literal
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
    """Convert supported spreadsheet files to CSV output."""

    def __init__(self, file: Path, output: Path | None = None, *, disable_cli: bool = False) -> None:
        """Initialize the converter.

        Args:
            file: Source file to convert.
            output: Optional target path for the generated CSV file.
            disable_cli: Disables interactive CLI prompts and CLI logging
                behavior when set to ``True``.
        """
        self.__file = file
        self.__output = output
        self.__disable_cli = disable_cli

    @property
    def output(self) -> Path:
        """Return the current output file path."""
        return self.__output

    @staticmethod
    def check_confidence_csv(detection: dict[str, str], filer: MainFiler, *, mute: bool = False) -> str:
        """Validate the detected CSV encoding before conversion.

        Args:
            detection: Raw result returned by the encoding detector.
            filer: File manager with metadata about the source file.
            mute: Skips the confirmation prompt when ``True``.

        Returns:
            str: Encoding selected for reading the CSV file.

        Raises:
            click.Abort: If confidence is low and the user declines to proceed.
        """
        verification = verify_confidence(detection)
        match verification['tag']:
            case 'high':
                logger.info(f'Confiabilidade [ {verification['value']:.2%} ]: Convertendo arquivo {filer.file.name}.')
            case 'medium':
                logger.warning(f'Confiabilidade [ {verification['value']:.2%} ]: Tentando converter arquivo {filer.file.name}.')
            case 'low':
                if not mute:
                    click.confirm(f'Confiança baixa [{verification['value']:.2%}]. Deseja continuar? y/n', abort=True)
                else:
                    logger.warning(f'<func: {DatafileConverter.check_confidence_csv.__name__}>: Low confidence {verification['value']:.2%}.')
        return verification['encoding']

    @staticmethod
    def save_new_csv(file: Path, output: Path, *, encoding: str = 'utf-8', file_type: Literal['csv', 'xlsx'] = 'xlsx') -> None:
        """Write a CSV file from a supported source file.

        Args:
            file: Source file to read.
            output: Destination path for the generated CSV file.
            encoding: Encoding used when reading CSV input files.
            file_type: Source file type. Supported values are ``"csv"`` and
                ``"xlsx"``.

        Raises:
            ValueError: If ``file_type`` is not supported.
            pandas.errors.ParserError: If pandas cannot parse the input file.
            FileNotFoundError: If the source file does not exist.
        """
        dataframe = None
        match file_type:
            case 'csv':
                dataframe = pd.read_csv(file, encoding=encoding, sep=None, engine='python')
            case 'xlsx':
                dataframe = pd.read_excel(file, engine='openpyxl')
        dataframe.to_csv(output, index=False, encoding='utf-8')
        return None

    def process(self):
        """Run the complete conversion workflow.

        Returns:
            None: Returns ``None`` after a successful conversion.

        Raises:
            FileNotFoundError: If the input file or temporary resources are
                missing.
            ValueError: If the input type or output path is invalid.
            Exception: Re-raises any unexpected error from the conversion flow.
        """
        try:
            logger.info(f'Convertendo [ {self.__file.name} ] em CSV')
            with MainFiler(file=self.__file, output=self.__output) as filer:
                self.__file = filer.validate_input_file()
                self.__output = filer.validate_output_file()
                suffix = filer.detect_suffix()
                if suffix == 'xlsx':
                    unzip_xlsx(filer.file, filer.temp_dir)
                    sanitize_spreadsheets(filer.temp_dir)
                    zip_xlsx(filer.temp_dir, filer.temp_file)
                    self.save_new_csv(filer.temp_file, filer.output)
                elif suffix == 'csv':
                    detection = detect_encoding(filer.file)
                    encoding = self.check_confidence_csv(detection, filer, mute=self.__disable_cli)
                    self.save_new_csv(filer.file, filer.output, encoding=encoding, file_type=suffix)
                else:
                    raise ValueError(f":method: {self.process.__name__} >> Type file not supported.")
                logger.info(f'Arquivo [ {filer.output.name} ] gerado em: {filer.output.parent.resolve()}')
            return None
        except Exception as error:
            if not self.__disable_cli:
                logger.error(f'{self.__class__.__name__}[ {error.__class__.__name__} ] >> {error.__str__()}')
            raise
