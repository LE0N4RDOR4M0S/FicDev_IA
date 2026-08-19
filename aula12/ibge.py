import requests

url = 'https://educa.ibge.gov.br/images/educa/jovens/materias-especiais/estimativa1.jpg'

resp = requests.get(url, timeout=30)
resp.raise_for_status()
# with open('imagem_ibge.jpg', 'wb') as arquivo:
#     arquivo.write(resp.content)
    
# print(f'Imagem salva: {len(resp.content) / 1024:.2f} KB')

with requests.get(url, stream=True) as resp:
    resp.raise_for_status()
    with open('imagem_ibge.jpg', 'wb') as arquivo:
        for chunk in resp.iter_content(chunk_size=1024):
            print(f'Mais um!')
            arquivo.write(chunk)
            