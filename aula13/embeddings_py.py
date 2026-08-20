import re
import unicodedata

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

def preprocessar_para_embedding(texto: str) -> str:
    """
    Preprocessa o texto para ser usado em embeddings, removendo acentos, caracteres especiais e espaços extras.
    
    Args:
        texto (str): O texto a ser preprocessado.
    Returns:
        str: O texto preprocessado.
    """
    if not texto or not texto.strip():
        return ''
    
    texto = limpar_texto(texto)
    texto = re.sub(r'https?://\S+', '[URL]', texto)
    texto = re.sub(r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b', '[EMAIL]', texto)
    texto = re.sub(r'\b\d{6,}\b', '[NUM]', texto)
    texto = re.sub(r'[\t]+', ' ', texto)
    print(texto.strip())
    return texto.strip()

texto_limpo = ''
with open('texto_limpo.txt', 'r', encoding='utf-8') as f:
    texto_limpo = f.read()
    
preprocessar_para_embedding(texto_limpo)
