# [csv-converter-skart](https://pypi.org/project/csv-converter-skart/)

[![PyPI Version](https://img.shields.io/pypi/v/csv-converter-skart?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/csv-converter-skart/)
[![Python Version](https://img.shields.io/pypi/pyversions/csv-converter-skart?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/csv-converter-skart/)
[![CI](https://img.shields.io/github/actions/workflow/status/SkyArtur/csv-converter-skart/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI)](https://github.com/SkyArtur/csv-converter-skart/actions/workflows/ci.yml)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SkyArtur/csv-converter-skart)

Ferramenta de linha de comando para converter e sanitizar arquivos de planilha, com foco em dados inconsistentes e geração de arquivos CSV com suporte a `pandas`.

[English version](./README.en.md)

## Visão geral

O projeto converte arquivos `.xlsx`, `.xls` e `.csv` para CSV, aplicando etapas de normalização úteis para cenários em que a origem contém problemas de estrutura, conteúdo ou codificação.

Principais recursos:

- Conversão de planilhas para CSV.
- Normalização de arquivos CSV com saída em UTF-8.
- Sanitização de XML interno de arquivos XLSX.
- Detecção de codificação para arquivos CSV.
- Interface de linha de comando e uso programático via módulo Python.

## Requisitos

- Python `>= 3.10`

## Instalação

```shell
pip install csv-converter-skart
```

## Uso

### Linha de comando

Se apenas o arquivo de entrada for informado, o diretório `File{NomeDoArquivo}Normalized` será criado no diretório atual. O CSV gerado manterá o nome base do arquivo original.

```shell
csv-converter ./meus_arquivos/arquivo.xlsx
```

Para definir explicitamente o arquivo de saída, use `-o` ou `--output`.

```shell
csv-converter ./meus_arquivos/arquivo.xlsx --output ./csv/arquivo_normalizado.csv
```

Para exibir a ajuda da CLI:

```shell
csv-converter --help
```

### Uso como módulo

O pacote também expõe a função `csv_converter`, que pode ser importada diretamente.

```python
import pandas as pd
from pathlib import Path

from csv_converter import csv_converter

input_file = Path("csv_converter/tests/fixtures/input_files/original.xlsx")
output_file = Path("csv_converter/tests/artifacts/original.csv")

generated_file = csv_converter(input_file, output_file)
dataframe = pd.read_csv(generated_file)

print(dataframe.info())
```

## Comportamento de saída

- Entradas `.xlsx` e `.xls` são processadas e exportadas para CSV.
- Entradas `.csv` são lidas com detecção de codificação e regravadas em UTF-8.
- Quando o caminho de saída não é informado, ele é criado automaticamente.

## Licença

MIT License - Copyright (c) 2026 [Artur dos Santos Shon](https://github.com/SkyArtur)