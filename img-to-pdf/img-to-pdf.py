import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_PADRAO_ORIGEM = os.path.join(BASE_DIR, "input")
PASTA_PADRAO_SAIDA = os.path.join(BASE_DIR, "output")
ARQUIVO_PDF_PADRAO = os.path.join(PASTA_PADRAO_SAIDA, "documento_final.pdf")


def imagens_para_pdf(pasta_origem=None, caminho_pdf_saida=None):
    """Converte todas as imagens de uma pasta em um único PDF."""
    if pasta_origem is None:
        pasta_origem = PASTA_PADRAO_ORIGEM

    if caminho_pdf_saida is None:
        os.makedirs(PASTA_PADRAO_SAIDA, exist_ok=True)
        caminho_pdf_saida = ARQUIVO_PDF_PADRAO

    if not os.path.exists(pasta_origem):
        print(f"Pasta de origem não encontrada: {pasta_origem}")
        return

    extensoes_suportadas = ('.jpg', '.jpeg', '.png', '.bmp')
    arquivos = sorted(os.listdir(pasta_origem))
    lista_imagens = []

    for arquivo in arquivos:
        if arquivo.lower().endswith(extensoes_suportadas):
            caminho_completo = os.path.join(pasta_origem, arquivo)
            img = Image.open(caminho_completo)

            if img.mode != 'RGB':
                img = img.convert('RGB')

            lista_imagens.append(img)

    if not lista_imagens:
        print(f"Nenhuma imagem encontrada na pasta: {pasta_origem}")
        return

    pasta_saida = os.path.dirname(caminho_pdf_saida)
    if pasta_saida and not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida, exist_ok=True)

    primeira_imagem = lista_imagens[0]
    imagens_restantes = lista_imagens[1:]

    primeira_imagem.save(
        caminho_pdf_saida,
        save_all=True,
        append_images=imagens_restantes
    )

    print(f"PDF criado com sucesso em: {caminho_pdf_saida}")


if __name__ == "__main__":
    import sys

    pasta_origem = sys.argv[1] if len(sys.argv) > 1 else PASTA_PADRAO_ORIGEM
    caminho_pdf_saida = sys.argv[2] if len(sys.argv) > 2 else ARQUIVO_PDF_PADRAO

    imagens_para_pdf(pasta_origem, caminho_pdf_saida)