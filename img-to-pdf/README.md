# Conversor de imagens para PDF

Este script lê todas as imagens de uma pasta, as ordena pelos nomes dos arquivos e salva tudo em um único arquivo PDF.

## Comportamento padrão

Se nenhum caminho for informado, o script usa automaticamente:

- origem: `input`
- saída: `output/documento_final.pdf`

Ou seja, a estrutura esperada é:

```text
img-to-pdf/
├── input/
│   ├── 01.jpg
│   ├── 02.png
│   └── ...
├── output/
├── img-to-pdf.py
├── README.md
└── ...
```

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

### 1) Usando os caminhos padrão

Coloque as imagens na pasta `input` e execute:

```bash
python img-to-pdf.py
```

O arquivo PDF será salvo em:

```text
output/documento_final.pdf
```

### 2) Informando caminhos personalizados

```bash
python img-to-pdf.py "C:/caminho/para/imagens" "C:/caminho/para/saida/meu_pdf.pdf"
```

ou também pode chamar a função em código:

```python
from img_to_pdf import imagens_para_pdf

imagens_para_pdf("C:/caminho/para/imagens", "C:/caminho/para/saida/meu_pdf.pdf")
```

## Exemplo

Se a pasta `input` contiver:

```text
input/
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
- A pasta `output` será criada automaticamente, se ainda não existir.
