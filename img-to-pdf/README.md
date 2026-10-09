# Conversor de imagens para PDF

Este script lê todas as imagens de uma pasta, as ordena pelos nomes dos arquivos e salva tudo em um único arquivo PDF.

## O que ele faz

- Busca imagens em uma pasta informada
- Aceita os formatos: `.jpg`, `.jpeg`, `.png` e `.bmp`
- Ordena os arquivos por nome para manter a sequência correta
- Converte imagens para RGB antes de salvar no PDF
- Gera um arquivo PDF com todas as imagens em sequência

## Requisitos

- Python 3.x
- Biblioteca Pillow

Instale a dependência com:

```bash
pip install pillow
```

## Como usar

1. Abra o arquivo `img-to-pdf.py`
2. Ajuste os caminhos da pasta de origem e do PDF de saída:

```python
PASTA_DAS_IMAGENS = r"C:\caminho\para\sua\pasta\de\imagens"
PDF_DE_SAIDA = r"C:\caminho\para\documento_final.pdf"
```

3. Execute o script:

```bash
python img-to-pdf.py
```

## Exemplo

Se a pasta contiver:

```text
imagens/
├── 01.jpg
├── 02.png
├── 03.jpeg
└── 04.bmp
```

Ao rodar o script, será gerado um PDF com as páginas na ordem:

```text
01.jpg
02.png
03.jpeg
04.bmp
```

## Observações

- A ordem das imagens segue a ordem alfabética dos nomes dos arquivos.
- Se não houver imagens na pasta informada, o script exibe uma mensagem e encerra.
- Imagens com transparência, como PNGs, são convertidas para RGB antes de entrar no PDF.

## Estrutura esperada

```text
img-to-pdf/
├── img-to-pdf.py
├── README.md
└── ...
```
