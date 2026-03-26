# [csv-converter-skart 0.1.2](https://pypi.org/project/csv-converter-skart/)

Ferramenta de linha de comando para conversão e sanitização de arquivos de planilhas, com foco no tratamento de dados inconsistentes e na geração de arquivos CSV por meio do Pandas.

## Instalação

```shell
pip install csv-converter-skart
```

## Utilização

> **Informando apenas o arquivo de entrada:** Se o destino não for definido, o diretório `File{NomeDoArquivo}Normalized` será criado no local em que o comando for executado. O arquivo CSV gerado terá o mesmo nome do arquivo original.

```shell
csv-converter ./meus_arquivos/arquivo.xlsx
```

> **Informando o arquivo de saída:** Use as flags `-o` ou `--output` para definir o destino do arquivo de saída.

```shell
csv-converter ./meus_arquivos/arquivo.xlsx -o ./csv/arquivo_normalizado.csv
```

> **Ajuda:**

```shell
csv-converter --help
```

## Licença

MIT License - Copyright (c) 2026 Artur dos Santos Shon
