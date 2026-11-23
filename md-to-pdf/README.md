# Markdown para PDF

Este script converte um arquivo `.md` em PDF, preservando a formatação Markdown, como títulos, listas, links, tabelas, citações e blocos de código. Também permite escolher um esquema de cores.

## Pré-requisitos e instalação

- Python 3.9 ou superior
- Dependências listadas em `requirements.txt`

Instale as dependências com:

```powershell
py -m pip install -r .\md-to-pdf\requirements.txt
```

## Como usar

O PDF é salvo por padrão na mesma pasta e com o mesmo nome do arquivo Markdown:

```powershell
py .\md-to-pdf\md-to-pdf.py "C:\docs\relatorio.md"
```

Informe outro caminho de saída com `-o` ou `--output`:

```powershell
py .\md-to-pdf\md-to-pdf.py "C:\docs\relatorio.md" -o "C:\output\relatorio.pdf"
```

Escolha um esquema de cores com `--theme`:

```powershell
py .\md-to-pdf\md-to-pdf.py "C:\docs\relatorio.md" --theme ocean
```

Temas disponíveis: `github` (padrão), `dark`, `sepia` e `ocean`. A pasta do arquivo PDF de saída deve existir.
