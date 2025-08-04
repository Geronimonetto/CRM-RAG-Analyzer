import json
import re

def anonimizar_texto(texto):
    # Remove CPF
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF REMOVIDO]', texto)

    # Remove telefone
    texto = re.sub(r'\(?\d{2}\)?[\s.-]?\d{4,5}[\s.-]?\d{4}', '[TELEFONE REMOVIDO]', texto)

    # Remove cartão de crédito
    texto = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[CARTAO REMOVIDO]', texto)

    # Remove nomes precedidos de "Nome:" ou "Cliente:"
    texto = re.sub(
        r'(?i)\b(Nome|Cliente)\s*[:：]\s*[A-ZÁ-Úa-zá-ú]{2,}(?:\s+[A-ZÁ-Úa-zá-ú]{2,}){1,4}',
        r'\1: [NOME REMOVIDO]',
        texto
    )

    # Remove nomes COMPLETOS em caixa alta (2 a 4 palavras com letras maiúsculas)
    texto = re.sub(
        r'\b(?:[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,}(?:\s+|$)){2,4}',
        '[NOME MAIÚSCULO REMOVIDO]',
        texto
    )

    return texto



# Caminho do arquivo JSON de entrada
arquivo_entrada = './data/raw/crm.json'

# Caminho do arquivo TXT de saída
arquivo_saida = './data/processed/crm_conversas_anonimizadas.txt'

# Lê o JSON
with open(arquivo_entrada, 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Escreve todas as conversas em um .txt
with open(arquivo_saida, 'w', encoding='utf-8') as f_out:
    for item in dados:
        texto_original = item.get("Coc Descricao", "")
        texto_limpo = anonimizar_texto(texto_original)
        f_out.write(texto_limpo.strip() + "\n\n" + "-"*50 + "\n\n")  # separador entre conversas
