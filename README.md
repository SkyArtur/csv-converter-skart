# [csv-converter-skart 0.1.2](https://test.pypi.org/project/csv-converter-skart/)

--- 

``Testes``

Ferramenta CLI para sanitização de dados inconsistentes em arquivos ``.xlsx``, auxiliando na conversão para csv, pelo
dataframe do Pandas. 

- Instalação:
```shell
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ csv-converter-skart
```

- Utilização:
Passando o arquivo a ser convertido, sem definir o destino, o diretório ``File{NomeDoArquivo}Normalized``, será criado 
no ponto de execução do comando, onde o arquivo csv será criado com o mesmo nome do arquivo original:
```shell
csv-converter ./meus_arquivos/arquivo.xlsx
```

Utilizando as flags ``-o`` ou ``--output`` para definir o destino do arquivo de saída:
```shell
csv-converter ./meus_arquivos/arquivo.xlsx -o ./csv/arquivo_normalizado.csv
```

Ajuda:
```shell
csv-converter --help
```

## Licença

MIT License — Copyright (c) 2026 Artur dos Santos Shon