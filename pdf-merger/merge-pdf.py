import os
from pypdf import PdfWriter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_PADRAO_ORIGEM = os.path.join(BASE_DIR, "input")
PASTA_PADRAO_SAIDA = os.path.join(BASE_DIR, "output")
ARQUIVO_PDF_PADRAO = os.path.join(PASTA_PADRAO_SAIDA, "all_combined.pdf")


def unir_pdfs(pasta_origem=None, caminho_pdf_saida=None):
    if pasta_origem is None:
        pasta_origem = PASTA_PADRAO_ORIGEM

    if caminho_pdf_saida is None:
        os.makedirs(PASTA_PADRAO_SAIDA, exist_ok=True)
        caminho_pdf_saida = ARQUIVO_PDF_PADRAO

    if not os.path.exists(pasta_origem):
        print(f"Pasta de origem não encontrada: {pasta_origem}")
        return

    writer = PdfWriter()

    arquivos_pdf = sorted(
        arquivo for arquivo in os.listdir(pasta_origem)
        if arquivo.lower().endswith(".pdf") and arquivo != os.path.basename(caminho_pdf_saida)
    )

    if not arquivos_pdf:
        print(f"Nenhum PDF encontrado na pasta: {pasta_origem}")
        return

    for arquivo in arquivos_pdf:
        caminho_arquivo = os.path.join(pasta_origem, arquivo)
        print(f"Anexando: {caminho_arquivo}")
        writer.append(caminho_arquivo)

    pasta_saida = os.path.dirname(caminho_pdf_saida)
    if pasta_saida and not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida, exist_ok=True)

    with open(caminho_pdf_saida, "wb") as arquivo_saida:
        writer.write(arquivo_saida)

    writer.close()
    print(f"PDF final criado em: {caminho_pdf_saida}")


if __name__ == "__main__":
    import sys

    pasta_origem = sys.argv[1] if len(sys.argv) > 1 else PASTA_PADRAO_ORIGEM
    caminho_pdf_saida = sys.argv[2] if len(sys.argv) > 2 else ARQUIVO_PDF_PADRAO

    unir_pdfs(pasta_origem, caminho_pdf_saida)