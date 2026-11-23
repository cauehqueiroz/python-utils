# Python Utilities

Este repositório reúne uma coleção de scripts em Python para tarefas rápidas e práticas de processamento de arquivos e geração de materiais visuais.

## Estrutura do projeto

```text
python/
├── README.md
├── img-to-pdf/
│   ├── README.md
│   ├── img-to-pdf.py
│   ├── input/
│   └── output/
├── md-to-pdf/
│   ├── README.md
│   ├── md-to-pdf.py
│   └── requirements.txt
├── pdf-merger/
│   └── merge-pdf.py
└── pix-generator/
    ├── README.md
    ├── pix-generator.py
    ├── logo_pix.png
    └── plaquinha_pix.png
```

## Scripts incluídos

### 1. img-to-pdf
Localizado em: `img-to-pdf/`

Converte imagens de uma pasta em um único arquivo PDF, preservando a ordem alfabética dos nomes dos arquivos.

Principais recursos:
- aceita `.jpg`, `.jpeg`, `.png` e `.bmp`
- ordena automaticamente as imagens
- cria a pasta de saída se necessário
- converte imagens para RGB antes de salvar no PDF

Uso:
```bash
cd img-to-pdf
python img-to-pdf.py
```

Mais detalhes em [img-to-pdf/README.md](./img-to-pdf/README.md).

### 2. pdf-merger
Localizado em: `pdf-merger/`

Une vários arquivos PDF de uma pasta em um único documento final.

Uso:
```bash
cd pdf-merger
python merge-pdf.py
```

Esse script usa a pasta `input` como origem padrão e salva o resultado em `output/all_combined.pdf` por padrão.

### 3. pix-generator
Localizado em: `pix-generator/`

Gera uma plaquinha de pagamento Pix com QR Code estático, incluindo dados do beneficiário e layout visual configurável.

Principais recursos:
- suporte a chave Pix por e-mail, CPF, CNPJ ou telefone
- geração automática do QR Code
- opção de personalização do tipo da chave
- saída em imagem PNG

Uso básico:
```bash
cd pix-generator
python pix-generator.py --chave 11999998888 --nome "João Silva"
```

Mais detalhes em [pix-generator/README.md](./pix-generator/README.md).

## Word to PDF

Convert Microsoft Word documents to PDF on Windows using Microsoft Word. See the [Word to PDF instructions](word-to-pdf/README.md) for requirements and usage.

## Markdown para PDF

Converte arquivos Markdown em PDF, preservando a formatação e permitindo escolher um esquema de cores. Consulte as [instruções do Markdown para PDF](md-to-pdf/README.md).

## Requisitos gerais

- Python 3.x
- Bibliotecas conforme cada script:

```bash
pip install pillow qrcode[pil] pypdf
```

## Como usar este repositório

1. Escolha a pasta do utilitário desejado.
2. Siga as instruções específicas de cada README.
3. Coloque os arquivos de entrada na estrutura esperada por cada script.
4. Execute o script com os parâmetros necessários.

## Objetivo

O repositório foi organizado para facilitar a criação de ferramentas simples e úteis para:
- conversão de arquivos
- automação de documentos
- geração de imagens e códigos de pagamento

Se quiser, também é possível adaptar os scripts para receber argumentos por linha de comando mais avançados ou transformar cada utilitário em uma CLI mais robusta.
