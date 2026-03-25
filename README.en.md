# csv-converter-skart 0.1.2

> Command-line tool for converting and sanitizing spreadsheet files, focused on handling inconsistent data and generating CSV files with Pandas.

## Installation

```shell
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ csv-converter-skart
```

## Usage

> **Providing only the input file:** If no destination is specified, the `File{OriginalFileName}Normalized` directory will be created in the location where the command is executed. The generated CSV file will keep the same name as the original file.

```shell
csv-converter ./my_files/file.xlsx
```

> **Providing the output file:** Use the `-o` or `--output` flags to define the output file path.

```shell
csv-converter ./my_files/file.xlsx -o ./csv/normalized_file.csv
```

> **Help:**

```shell
csv-converter --help
```

## License

> MIT License - Copyright (c) 2026 Artur dos Santos Shon
