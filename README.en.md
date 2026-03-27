# [csv-converter-skart](https://pypi.org/project/csv-converter-skart/)

[![PyPI Version](https://img.shields.io/pypi/v/csv-converter-skart?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/csv-converter-skart/)
[![Python Version](https://img.shields.io/pypi/pyversions/csv-converter-skart?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/csv-converter-skart/)
[![CI](https://img.shields.io/github/actions/workflow/status/SkyArtur/csv-converter-skart/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI)](https://github.com/SkyArtur/csv-converter-skart/actions/workflows/ci.yml)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SkyArtur/csv-converter-skart)

Command-line tool for converting and sanitizing spreadsheet files, with a focus on inconsistent data and CSV generation backed by `pandas`.

[Versão em português](./README.md)

## Overview

This project converts `.xlsx`, `.xls`, and `.csv` files to CSV while applying normalization steps that are useful when the source data contains structural, content, or encoding issues.

Key features:

- Convert spreadsheet files to CSV.
- Normalize CSV files and rewrite them as UTF-8.
- Sanitize internal XML content from XLSX files.
- Detect text encoding for CSV inputs.
- Use the project through both a CLI and a Python module.

## Requirements

- Python `>= 3.10`

## Installation

```shell
pip install csv-converter-skart
```

## Usage

### Command line

If only the input file is provided, the `File{OriginalFileName}Normalized` directory is created in the current working directory. The generated CSV keeps the original base filename.

```shell
csv-converter ./my_files/file.xlsx
```

To define the output file explicitly, use `-o` or `--output`.

```shell
csv-converter ./my_files/file.xlsx --output ./csv/normalized_file.csv
```

To display the CLI help:

```shell
csv-converter --help
```

### Module usage

The package also exposes the `csv_converter` function for direct import.

```python
import pandas as pd
from pathlib import Path

from csv_converter import csv_converter

input_file = Path("./meu_arquivo.xlsx")
output_file = Path("./saida.csv")

generated_file = csv_converter(input_file, output_file)
dataframe = pd.read_csv(generated_file)

print(dataframe.info())
```

## Output behavior

- `.xlsx` and `.xls` inputs are processed and exported to CSV.
- `.csv` inputs are read with encoding detection and rewritten as UTF-8.
- When no output path is provided, one is created automatically.

## License

MIT License - Copyright (c) 2026 [Artur dos Santos Shon](https://github.com/SkyArtur)
