from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

def ocr_pdf(caminho_pdf: str,
            dpi: int = 300,
            idioma: str = 'por',
            psm: int = 6) -> str:
    """
    Args:
        caminho_pdf: Caminho para o arquivo PDF.
        dpi: Resolução em DPI para conversão de PDF para imagem.
        idioma: Código do idioma para OCR (ex: 'por' para português).
        psm: Page Segmentation Mode do Tesseract (0-13).
    Returns:
        Texto extraído do PDF.
    """
    
    print(f"Convertendo PDF para imagens (DPI={dpi})...")
    paginas = convert_from_path(
        caminho_pdf,
        dpi=dpi,
        fmt='png',             # PNG preserva qualidade (sem compressão JPEG)
        thread_count=4,        # paralelismo na conversão
    )

    print(f'Total de paginas: {len(paginas)}')
    config_tess = f'--oem 3 --psm {psm} -l {idioma}'
    resultados  = []

    for i, img_pagina in enumerate(paginas, start=1):
        print(f'  Processando pagina {i}/{len(paginas)}...', end=' ')

        texto = pytesseract.image_to_string(img_pagina, config=config_tess)
        texto = texto.strip()

        resultados.append({
            'pagina':     i,
            'texto':      texto,
            'caracteres': len(texto),
        })
        print(f'{len(texto)} caracteres')

    return resultados

def salvar_texto_pdf(resultados: list[dict], destino: str) -> None:
    """Salva o texto extraído de todas as páginas em um único arquivo .txt."""
    with open(destino, 'w', encoding='utf-8') as arq:
        for r in resultados:
            arq.write(f'=== Página {r["pagina"]} ===\n')
            arq.write(r['texto'])
            arq.write('\n\n')
    total = sum(r['caracteres'] for r in resultados)
    print(f'Texto salvo em: {destino} ({total} caracteres no total)')


# Uso
resultados = ocr_pdf('035599_COMPLETO.pdf', dpi=300)
salvar_texto_pdf(resultados, 'contrato_extraido.txt')

# Texto completo concatenado
texto_completo = '\n\n'.join(r['texto'] for r in resultados)
