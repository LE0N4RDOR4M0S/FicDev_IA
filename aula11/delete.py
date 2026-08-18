import sqlite3

#UPDATE DE REGSITROS
# Aqui eu quero colocar todos os documentos que possuem tokens como processado
with sqlite3.connect('pipeline.db') as conn:
    conn.execute('''
                UPDATE documentos
                SET status = ?
                WHERE 1=1
                AND id < ?
                 ''', ('pendente', 10))

## DELETAR OS REGISTROS PENDENTES
with sqlite3.connect('pipeline.db') as conn:
    conn.execute('''
                DELETE FROM documentos
                WHERE 1=1
                AND status = ?
                 ''', ('pendente',))
    print('Registros deletados.')