import argparse
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont

def gerar_payload_pix(chave, beneficiario="Joao Silva", cidade="SAO PAULO", tipo="auto", valor=None):
    """
    Gera a string padrão do Pix Estático (BR Code EMV).
    Suporta o parâmetro opcional de valor.
    """
    chave_processada = str(chave).strip()
    apenas_numeros = "".join(filter(str.isdigit, chave_processada))
    
    is_telefone = tipo == "telefone" or (tipo == "auto" and "@" not in chave_processada and (len(apenas_numeros) == 10 or len(apenas_numeros) == 11))
    
    if is_telefone:
        if (len(apenas_numeros) == 10 or len(apenas_numeros) == 11) and not apenas_numeros.startswith("55"):
            chave_processada = f"+55{apenas_numeros}"
        else:
            chave_processada = f"+{apenas_numeros}" if not chave_processada.startswith("+") else chave_processada
    else:
        if "@" not in chave_processada and "." not in chave_processada:
            chave_processada = apenas_numeros

    gui = "BR.GOV.BCB.PIX"
    merchant_info = f"00{len(gui):02d}{gui}01{len(chave_processada):02d}{chave_processada}"
    
    payloads = {
        "00": "01",
        "26": merchant_info,
        "52": "0000",
        "53": "986",                                # BRL
        "58": "BR",
        "59": beneficiario[:25],
        "60": cidade[:15],
        "62": "0503***"
    }
    
    # Adiciona o valor se ele for informado e maior que zero
    if valor and float(valor) > 0:
        valor_str = f"{float(valor):.2f}"
        payloads["54"] = valor_str                  # ID 54: Transaction Amount
    
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
    tipo_param = tipo_param.lower().strip()
    if tipo_param in ["email", "e-mail"]: return "E-mail"
    elif tipo_param == "cpf": return "CPF"
    elif tipo_param == "cnpj": return "CNPJ"
    elif tipo_param == "telefone": return "Telefone"
        
    apenas_numeros = len("".join(filter(str.isdigit, chave)))
    if "@" in chave: return "E-mail"
    elif apenas_numeros == 11: return "CPF"
    elif apenas_numeros == 14: return "CNPJ"
    elif apenas_numeros == 10 or apenas_numeros == 11 or apenas_numeros == 13: # Com ou sem o prefixo 55
        return "Telefone"
    else:
        return "CNPJ" # Fallback padrão

def criar_imagem_plaquinha_pix(chave, nome_beneficiario, tipo_chave_param="auto", valor=None, salvar_como="plaquinha_pix.png"):
    # Expandimos levemente a altura se houver valor para manter o respiro visual
    largura = 450
    altura = 760 if (valor and float(valor) > 0) else 720
    
    background_color = "#FFFFFF"
    text_color = "#1A1A1A"
    pix_verde_escuro = "#0C514C"
    pix_bg_campo = "#E6F7F5"
    
    img = Image.new("RGB", (largura, altura), color=background_color)
    canvas = ImageDraw.Draw(img)
    
    try:
        font_titulo = ImageFont.truetype("GOTHICB.TTF", 36)
        font_sub = ImageFont.truetype("GOTHICB.TTF", 22)
        font_dados = ImageFont.truetype("GOTHIC.TTF", 18)
        font_valor = ImageFont.truetype("GOTHICB.TTF", 28)
    except IOError:
        try:
            font_titulo = ImageFont.truetype("ARIALBD.TTF", 36)
            font_sub = ImageFont.truetype("ARIALBD.TTF", 22)
            font_dados = ImageFont.truetype("ARIAL.TTF", 18)
            font_valor = ImageFont.truetype("ARIALBD.TTF", 28)
        except IOError:
            font_titulo = font_sub = font_dados = font_valor = ImageFont.load_default()

    # 1. Título do Topo
    canvas.text((largura/2, 60), "Pagamento Pix", fill=pix_verde_escuro, font=font_titulo, anchor="mm")
    
    # 2. Inserção do Logo Oficial
    logo_path = "logo_pix.png"
    if os.path.exists(logo_path):
        with Image.open(logo_path) as logo:
            logo_rgb = logo.convert("RGB")
            base_width = 200  
            w_percent = (base_width / float(logo_rgb.size[0]))
            h_size = int((float(logo_rgb.size[1]) * float(w_percent)))
            logo_resized = logo_rgb.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            logo_x = (largura - logo_resized.width) // 2
            logo_y = 100
            img.paste(logo_resized, (logo_x, logo_y))
    else:
        canvas.text((largura/2, 130), "✨ pix ✨", fill="#00B494", font=font_sub, anchor="mm")
    
    # 3. Geração e colagem do QR Code
    payload = gerar_payload_pix(chave=chave, beneficiario=nome_beneficiario, tipo=tipo_chave_param, valor=valor)
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color=background_color)
    qr_img = qr_img.resize((260, 260)) 
    
    pos_x = (largura - qr_img.width) // 2
    pos_y = 210
    img.paste(qr_img, (pos_x, pos_y))
    
    # Deslocamento vertical dinâmico baseado na presença do valor
    y_offset = 0
    
    # 4. Campo Opcional de Valor Informativo
    if valor and float(valor) > 0:
        valor_formatado = f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        canvas.text((largura/2, 500), "Valor", fill=pix_verde_escuro, font=font_sub, anchor="mm")
        canvas.text((largura/2, 535), valor_formatado, fill=text_color, font=font_valor, anchor="mm")
        y_offset = 65 # Empurra os campos de baixo para não encavalar
    
    # 5. Caixa de dados da Chave
    canvas.text((largura/2, 500 + y_offset), "Chave Pix", fill=pix_verde_escuro, font=font_sub, anchor="mm")
    
    box_y_start = 530 + y_offset
    canvas.rounded_rectangle([35, box_y_start, largura-35, box_y_start+55], radius=12, fill=pix_bg_campo)
    
    label_formatada = identificar_label_chave(chave, tipo_chave_param)
    texto_chave = f"{label_formatada}: {chave}"
    
    canvas.text((largura/2, box_y_start+27), texto_chave, fill=pix_verde_escuro, font=font_dados, anchor="mm")
    
    # Nome do recebedor
    canvas.text((largura/2, 635 + y_offset), nome_beneficiario.upper(), fill=pix_verde_escuro, font=font_sub, anchor="mm")
    
    img.save(salvar_como)
    print(f"🎉 Sucesso! Plaquha gerada com valor e salva como '{salvar_como}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador Customizado de Plaquha Pix")
    
    parser.add_argument("--chave", required=True, help="Sua chave Pix")
    parser.add_argument("--nome", required=True, help="Nome do beneficiário")
    parser.add_argument("--tipo", default="auto", choices=["auto", "email", "cpf", "cnpj", "telefone"], help="Forçar tipo da chave")
    parser.add_argument("--valor", type=float, default=None, help="Valor cobrado (opcional, ex: 15.90)")
    parser.add_argument("--saida", default="plaquinha_pix.png", help="Nome do arquivo de saída")

    args = parser.parse_args()

    criar_imagem_plaquinha_pix(
        chave=args.chave, 
        nome_beneficiario=args.nome, 
        tipo_chave_param=args.tipo,
        valor=args.valor,
        salvar_como=args.saida
    )
