import os
from PIL import Image

def imagens_para_pdf(pasta_origem, caminho_pdf_saida):
    # Extensões de imagem suportadas
    extensoes_suportadas = ('.jpg', '.jpeg', '.png', '.bmp')
    
    # Lista e ordena os arquivos para manter a sequência correta
    arquivos = sorted(os.listdir(pasta_origem))
    
    lista_imagens = []
    
    for arquivo in arquivos:
        if arquivo.lower().endswith(extensoes_suportadas):
            caminho_completo = os.path.join(pasta_origem, arquivo)
            
            # Abre a imagem
            img = Image.open(caminho_completo)
            
            # Garante que a imagem está no modo RGB (essencial para PNGs com transparência/RGBA)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            lista_imagens.append(img)
            
    if not lista_imagens:
        print("Nenhuma imagem encontrada na pasta especificada.")
        return

    # O truque do Pillow: pega a primeira imagem e apenda o resto usando 'save_all=True'
    primeira_imagem = lista_imagens[0]
    imagens_restantes = lista_imagens[1:]
    
    primeira_imagem.save(
        caminho_pdf_saida,
        save_all=True,
        append_images=imagens_restantes
    )
    
    print(f"PDF criado com sucesso em: {caminho_pdf_saida}")

# --- Configuração de Uso ---
PASTA_DAS_IMAGENS = "caminho/para/sua/pasta/de/imagens"
PDF_DE_SAIDA = "documento_final.pdf"

# Executa a função
imagens_para_pdf(PASTA_DAS_IMAGENS, PDF_DE_SAIDA)