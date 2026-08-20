import pdfplumber

with pdfplumber.open('83800_por.pdf') as pdf:

    # Metadados
    print(pdf.metadata)
    print(f'{len(pdf.pages)} páginas')

    # Extrair texto de uma página
    pagina = pdf.pages[0]
    texto = pagina.extract_text()
    print(texto[:500])
    texto = pagina.extract_text(x_tolerance=3, y_tolerance=3)

    print(texto[:500])

    paginas = []
    for i, pag in enumerate(pdf.pages):
        texto = pag.extract_text() or ''
        paginas.append({'pagina': i + 1, 'texto': texto})