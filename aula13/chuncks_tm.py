from minilab.src.extrator.pipeline import limpar_texto


def chunks_por_tamanho(
texto: str,
tamanho_max: int = 1000,
overlap: int = 200,
origem: str = '',
) -> list[dict]:
    """
    Recebe um texto e retorna uma lista de chunks, cada um com tamanho máximo de tamanho_max.
    Se o texto for maior que tamanho_max, os chunks terão overlap de overlap caracteres.
    Cada chunk é um dicionário com as chaves:
        - 'chunk_id': id do chunk, no formato 'origem_pagina_chunk'
        - 'texto': o texto do chunk
        - 'n_chars': número de caracteres do chunk
        - 'inicio': posição inicial do chunk no texto original
        - 'fim': posição final do chunk no texto original
    """
    texto = limpar_texto(texto)
    if not texto:
        return []

    chunks = []
    inicio = 0
    idx = 0

    while inicio < len(texto):
        fim = inicio + tamanho_max
        trecho = texto[inicio:fim]
    
        if fim < len(texto):
            ultimo_espaco = trecho.rfind(' ')
            if ultimo_espaco > tamanho_max * 0.6:
                trecho = trecho[:ultimo_espaco]
                fim = inicio + ultimo_espaco
        chunks.append({
            'chunk_id': f'{origem}_c{idx:03d}' if origem else f'c{idx:03d}',
            'texto': trecho.strip(),
            'n_chars': len(trecho.strip()),
            'inicio': inicio,
            'fim': inicio + len(trecho)
        })
        
        inicio = fim -overlap
        idx += 1
    return chunks