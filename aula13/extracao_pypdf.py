from pypdf import PdfReader

reader = PdfReader('83800_por.pdf')

meta = reader.metadata
print(meta.title)
print(meta.author)
print(meta.creation_date)
print(meta.producer)

print(f'Numero de paginas: {len(reader.pages)}')

if (reader.is_encrypted):
    print('O arquivo PDF está protegido.')
    reader.decrypt('senha')
    
pagina = reader.pages[100]
print('Largura da página: ', pagina.mediabox.width)
print('Altura da página: ', pagina.mediabox.height)

print('Texto da primeira página: ', pagina.extract_text())