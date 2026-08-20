import limpar_texto

def chucks_por_pagina(paginas: list[dict]) -> list[dict]:
    """
    Recebe uma lista de { 'pagina': N, 'texto': '...'}
    Retorna a mesma lista, pulando páginas vazias.
    return [
            {
                'chunk_id': f'p{p["pagina"]:03d}',
                'pagina': p['pagina'],
                'texto': limpar_texto(p['texto']),
                'n_chars': len(p['texto']),
            }
        ]
    """
    
    for p in paginas:
        if p['texto'].strip():
            yield {
                'chunk_id': f'p{p["pagina"]:03d}',
                'pagina': p['pagina'],
                'texto': limpar_texto(p['texto']),
                'n_chars': len(p['texto']),
            }
    
    