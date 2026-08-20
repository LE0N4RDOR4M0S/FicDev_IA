import pdfplumber

with pdfplumber.open('83800_por.pdf') as pdf:
    pagina = pdf.pages[0]

    palavras = pagina.extract_words()
    for palavra in palavras[:5]:
        print(palavra)

    altura = float(pagina.height)
    corpo = pagina.crop((0, 80, pagina.width, altura - 80))
    texto_corpo = corpo.extract_text() or ''
    print(f'Texto do corpo: {len(texto_corpo)} caracteres')

    textos_limpos = []
    for pag in pdf.pages:
        recorte = pag.crop((0, 60, pag.width, float(pag.height) - 60))
        textos_limpos.append(recorte.extract_text() or '')