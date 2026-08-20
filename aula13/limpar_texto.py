import re
import unicodedata
import pdfplumber

def limpar_texto(texto: str) -> str:
    """
    Limpa o texto removendo acentos, caracteres especiais e espaços extras.
    
    Args:
        texto (str): O texto a ser limpo.

    Returns:
        str: O texto limpo.
    """
    if not texto or not texto.strip():
        return ''
    texto = unicodedata.normalize('NFC', texto)
    texto = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', texto)
    texto = re.sub(r'(\w+)-\n(\w+)', r'\1\2', texto)
    texto = re.sub(r'(?<!\n)\n(?!\n)', ' ', texto)
    texto = re.sub(r'[ \t]+', ' ', texto)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    texto = re.sub(r' +([.,;:!?])', r'\1', texto)
    
    return texto.strip()

with pdfplumber.open('381137por.pdf') as pdf:
    textos_limpos = []
    for pag in pdf.pages:
        recorte = pag.crop((0, 60, pag.width, float(pag.height) - 60))
        texto = recorte.extract_text() or ''
        texto_limpo = limpar_texto(texto)
        textos_limpos.append(texto_limpo)
        
#Criar um txt com o texto limpo
with open('texto_limpo.txt', 'w', encoding='utf-8') as f:
    for texto in textos_limpos:
        f.write(texto + '\n\n')