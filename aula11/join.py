import sqlite3

## FAZER JOIN ENTRE TABELAS
with sqlite3.connect('pipeline.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.id, d.nome, d.origem, d.status, d.num_tokens, t.token
        FROM documentos d
        INNER JOIN tokens t ON d.id = t.documento_id
    ''')
    registros = cursor.fetchall()
    for registro in registros:
        print(registro)