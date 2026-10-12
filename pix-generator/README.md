# Gerador de Plaquinha de Pagamento Pix com QR Code

Este projeto é um utilitário em Python executável via linha de comando para gerar uma **imagem customizada de balcão (plaquinha)** para recebimento de pagamentos via Pix. O código monta o layout de forma automatizada, gerencia o logotipo oficial, padroniza as identificações e gera o QR Code no padrão **Pix Estático** (especificação BR Code do Banco Central).

## 🚀 Novas Funcionalidades

1. **Logotipo Oficial Integrado:** O script agora carrega um arquivo de imagem externa (`logo_pix.png`), preservando transparências (canal Alpha) e redimensionando de forma proporcional para um acabamento profissional.
2. **Parâmetro de Tipo Opcional:** Você pode deixar o script detectar o tipo de chave de forma automática (padrão) ou forçar uma categoria específica usando a flag `--tipo`.
3. **Labels Padronizadas:** A descrição na caixa de dados exibe de forma limpa as nomenclaturas padrão: `Telefone`, `E-mail`, `CPF` ou `CNPJ`.
4. **Formatação Inteligente de Telefone:** Não há necessidade de digitar o código internacional do país (`55`) ao passar uma chave de celular. O script aceita apenas o `[DDD + Número]`, faz o ajuste em background para gerar o QR Code correto exigido pelo Banco Central e mantém a exibição visual limpa no rodapé da plaquinha.

---

## 🛠️ Pré-requisitos e Instalação

Certifique-se de ter o Python instalado em sua máquina. Em seguida, instale as dependências executando o comando abaixo no terminal:

```bash
pip install qrcode[pil] Pillow
```

### 📦 Preparação do Repositório
Para que o logotipo oficial seja renderizado no topo da plaquinha, salve a imagem do logo do Pix na mesma pasta do script com o nome exato de **`logo_pix.png`**. 
*(Caso o arquivo não seja encontrado, o script usará um texto alternativo estilizado automaticamente como fallback).*

---

## 💻 Como Usar

Passe as informações de forma dinâmica através de parâmetros (flags) no terminal ao rodar o script.

### Parâmetros Disponíveis

* `--chave` *(Obrigatório)*: A sua chave Pix (E-mail, CPF, CNPJ ou Telefone).
* `--nome` *(Obrigatório)*: Nome do beneficiário (titular da conta).
* `--tipo` *(Opcional)*: Força o tipo de chave informado. Opções: `auto`, `email`, `cpf`, `cnpj`, `telefone`. (Padrão: `auto`).
* `--saida` *(Opcional)*: Nome ou caminho do arquivo de imagem final. (Padrão: `plaquinha_pix.png`).

### Exemplos de Execução

**Gerando Telefone apenas com DDD (Detecção Automática):**
```bash
python pix-generator.py --chave 11999998888 --nome "João Silva"
```
*(O QR Code será gerado corretamente com o prefixo +5511999998888 por trás dos panos, mas a plaquinha exibirá o número exatamente como digitado).*

**Forçando o Tipo da Chave (Evita conflitos de detecção):**
```bash
python pix-generator.py --chave 12.345.678/0001-99 --nome "Minha Empresa LTDA" --tipo cnpj
```

**Definindo um nome personalizado para o arquivo de saída:**
```bash
python pix-generator.py --chave carlos@email.com --nome "Carlos Souza" --saida plaquinha_carlos.png
```

---

## 📌 Estrutura da Plaquinha Gerada

* **Cabeçalho:** Identificação textual "Pagamento Pix" acompanhado do logotipo oficial centralizado.
* **Centro:** QR Code em tamanho otimizado para leitura rápida por câmeras de qualquer smartphone.
* **Rodapé:** Bloco arredondado em tom neutro contendo a etiqueta exata do tipo da chave (`Telefone`, `E-mail`, `CPF` ou `CNPJ`) e o nome do titular da conta logo abaixo.

---

## 🔒 Segurança e Privacidade

Este script roda de forma **100% local**. Nenhum dado de sua chave Pix ou nome é enviado para APIs externas. Todo o processamento visual e o cálculo matemático do código de barras ocorrem exclusivamente na sua máquina.
