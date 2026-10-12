import argparse
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont

def gerar_payload_pix(chave, beneficiario="Joao Silva", cidade="SAO PAULO", tipo="auto"):
    """
    Gera a string padrão do Pix Estático (BR Code EMV).
    Trata chaves de telefone sem o código do país (55).
    """
    chave_processada = str(chave).strip()
    
    # Se for telefone (ou detectado como tal), garante o prefixo 55 exigido pelo BC
    apenas_numeros = "".join(filter(str.isdigit, chave_processada))
    
    is_telefone = tipo == "telefone" or (tipo == "auto" and "@" not in chave_processada and (len(apenas_numeros) == 10 or len(apenas_numeros) == 11))
    
    if is_telefone:
        # Se tem 10 ou 11 dígitos, o usuário enviou apenas [DDD + Número]. Adiciona o 55.
        if (len(apenas_numeros) == 10 or len(apenas_numeros) == 11) and not apenas_numeros.startswith("55"):
            chave_processada = f"+55{apenas_numeros}"
        else:
            chave_processada = f"+{apenas_numeros}" if not chave_processada.startswith("+") else chave_processada
    else:
        # Para CPF, CNPJ ou chaves numéricas gerais, remove pontuações
        if "@" not in chave_processada and "." not in chave_processada:
            chave_processada = apenas_numeros

    gui = "BR.GOV.BCB.PIX"
    merchant_info = f"00{len(gui):02d}{gui}01{len(chave_processada):02d}{chave_processada}"
    
    payloads = {
        "00": "01",
        "26": merchant_info,
        "52": "0000",
        "53": "986",
        "58": "BR",
        "59": beneficiario[:25],
        "60": cidade[:15],
        "62": "0503***"
    }
    
    string_payload = "".join([f"{k}{len(v):02d}{v}" for k, v in sorted(payloads.items())])
    string_payload += "6304"
    
    crc = 0xFFFF
    for char in string_payload:
        crc ^= (ord(char) << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
            
    return string_payload + f"{crc:04X}"

def identificar_label_chave(chave, tipo_param):
    """
    Retorna o texto exato da Label baseado no parâmetro informado ou na auto-detecção.
    """
    tipo_param = tipo_param.lower().strip()
    
    if tipo_param in ["email", "e-mail"]:
        return "E-mail"
    elif tipo_param == "cpf":
        return "CPF"
    elif tipo_param == "cnpj":
        return "CNPJ"
    elif tipo_param == "telefone":
        return "Telefone"
        
    # Lógica de auto-detecção corrigida (sem usar o operador 'in' incompleto)
    apenas_numeros = len("".join(filter(str.isdigit, chave)))
    if "@" in chave:
        return "E-mail"
    elif apenas_numeros == 11:
        return "CPF"
    elif apenas_numeros == 14:
        return "CNPJ"
    elif apenas_numeros == 10 or apenas_numeros == 11 or apenas_numeros == 13: # Com ou sem o prefixo 55
        return "Telefone"
    else:
        return "CNPJ" # Fallback padrão

def criar_imagem_plaquinha_pix(chave, nome_beneficiario, tipo_chave_param="auto", salvar_como="plaquinha_pix.png"):
    largura, altura = 400, 650
    background_color = "#f4eae6"
    text_color = "#1a1a1a"
    
    img = Image.new("RGB", (largura, altura), color=background_color)
    canvas = ImageDraw.Draw(img)
    
    try:
        font_titulo = ImageFont.truetype("arial.ttf", 32)
        font_sub = ImageFont.truetype("arial.ttf", 18)
        font_dados = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font_titulo = font_sub = font_dados = ImageFont.load_default()

    # 1. Título do Topo
    canvas.text((largura/2, 50), "Pagamento Pix", fill=text_color, font=font_titulo, anchor="mm")
    
    # 2. Inserção do Logo Oficial com Conversão Robusta para RGBA
    logo_path = "logo_pix.png"
    if os.path.exists(logo_path):
        with Image.open(logo_path) as logo:
            # Força a conversão para RGBA para evitar erros de paleta e transparência indexada
            logo_rgba = logo.convert("RGBA")
            
            base_width = 160
            w_percent = (base_width / float(logo_rgba.size[0]))
            h_size = int((float(logo_rgba.size[1]) * float(w_percent)))
            logo_resized = logo_rgba.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            logo_x = (largura - logo_resized.width) // 2
            logo_y = 90
            
            # Utiliza a própria imagem RGBA convertida como máscara (garante transparência perfeita)
            img.paste(logo_resized, (logo_x, logo_y), logo_resized)
    else:
        canvas.text((largura/2, 110), "✨ pix ✨", fill="#00b494", font=font_titulo, anchor="mm")
    
    # 3. Geração e colagem do QR Code
    payload = gerar_payload_pix(chave=chave, beneficiario=nome_beneficiario, tipo=tipo_chave_param)
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color=background_color)
    qr_img = qr_img.resize((220, 220))
    
    pos_x = (largura - qr_img.width) // 2
    pos_y = 190
    img.paste(qr_img, (pos_x, pos_y))
    
    # 4. Caixa de dados e Identificação de Tipo
    canvas.text((largura/2, 450), "Chave Pix", fill=text_color, font=font_sub, anchor="mm")
    
    box_y_start = 480
    canvas.rounded_rectangle([40, box_y_start, largura-40, box_y_start+40], radius=8, fill="#e8ded9")
    
    label_formatada = identificar_label_chave(chave, tipo_chave_param)
    texto_chave = f"{label_formatada}: {chave}"
    
    canvas.text((largura/2, box_y_start+20), texto_chave, fill=text_color, font=font_dados, anchor="mm")
    canvas.text((largura/2, 575), nome_beneficiario, fill=text_color, font=font_sub, anchor="mm")
    
    img.save(salvar_como)
    print(f"🎉 Sucesso! Imagem salva como '{salvar_como}'")

    largura, altura = 400, 650
    background_color = "#f4eae6"
    text_color = "#1a1a1a"
    
    img = Image.new("RGB", (largura, altura), color=background_color)
    canvas = ImageDraw.Draw(img)
    
    try:
        font_titulo = ImageFont.truetype("arial.ttf", 32)
        font_sub = ImageFont.truetype("arial.ttf", 18)
        font_dados = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font_titulo = font_sub = font_dados = ImageFont.load_default()

    # 1. Título do Topo
    canvas.text((largura/2, 50), "Pagamento Pix", fill=text_color, font=font_titulo, anchor="mm")
    
    # 2. Inserção do Logo Oficial
    logo_path = "logo_pix.png"
    if os.path.exists(logo_path):
        with Image.open(logo_path) as logo:
            base_width = 160
            w_percent = (base_width / float(logo.size[0]))
            h_size = int((float(logo.size[1]) * float(w_percent)))
            logo_resized = logo.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            logo_x = (largura - logo_resized.width) // 2
            logo_y = 90
            
            if logo_resized.mode in ('RGBA', 'LA') or (logo_resized.mode == 'P' and 'transparency' in logo_resized.info):
                img.paste(logo_resized, (logo_x, logo_y), logo_resized)
            else:
                img.paste(logo_resized, (logo_x, logo_y))
    else:
        canvas.text((largura/2, 110), "✨ Pix ✨", fill="#00b494", font=font_titulo, anchor="mm")
    
    # 3. Geração e colagem do QR Code
    payload = gerar_payload_pix(chave=chave, beneficiario=nome_beneficiario, tipo=tipo_chave_param)
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color=background_color)
    qr_img = qr_img.resize((220, 220))
    
    pos_x = (largura - qr_img.width) // 2
    pos_y = 190
    img.paste(qr_img, (pos_x, pos_y))
    
    # 4. Caixa de dados e Identificação de Tipo
    canvas.text((largura/2, 450), "Chave Pix", fill=text_color, font=font_sub, anchor="mm")
    
    box_y_start = 480
    canvas.rounded_rectangle([40, box_y_start, largura-40, box_y_start+40], radius=8, fill="#e8ded9")
    
    label_formatada = identificar_label_chave(chave, tipo_chave_param)
    texto_chave = f"{label_formatada}: {chave}"
    
    canvas.text((largura/2, box_y_start+20), texto_chave, fill=text_color, font=font_dados, anchor="mm")
    canvas.text((largura/2, 575), nome_beneficiario, fill=text_color, font=font_sub, anchor="mm")
    
    img.save(salvar_como)
    print(f"🎉 Sucesso! Imagem salva como '{salvar_como}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador Customizado de Plaquinha Pix")
    
    parser.add_argument("--chave", required=True, help="Sua chave Pix")
    parser.add_argument("--nome", required=True, help="Nome do beneficiário")
    parser.add_argument("--tipo", default="auto", choices=["auto", "email", "cpf", "cnpj", "telefone"], 
                        help="Forçar tipo da chave. Padrão: auto (detecta sozinho)")
    parser.add_argument("--saida", default="plaquinha_pix.png", help="Nome do arquivo de saída")

    args = parser.parse_args()

    criar_imagem_plaquinha_pix(
        chave=args.chave, 
        nome_beneficiario=args.nome, 
        tipo_chave_param=args.tipo,
        salvar_como=args.saida
    )
