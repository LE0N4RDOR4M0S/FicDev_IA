import sqlite3
from pathlib import Path
 
# Conectar (cria o arquivo se não existir)
conn = sqlite3.connect('pipeline.db')
 
# cursor executa instruções SQL
cursor = conn.cursor()
 
# Boa prática: usar como gerenciador de contexto
# O 'with' faz commit automático em sucesso e rollback em exceção
with sqlite3.connect('pipeline.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT sqlite_version()')
    print(cursor.fetchone())
 
# row_factory: retorna dicionários em vez de tuplas
conn = sqlite3.connect('pipeline.db')
conn.row_factory = sqlite3.Row   # acesso por nome: row['coluna']


## CRIAÇÃO DE TABELA
with sqlite3.connect('pipeline.db') as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT    NOT NULL,
            origem      TEXT    NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'pendente',
            num_tokens  INTEGER,
            criado_em   TEXT    DEFAULT (datetime('now','localtime'))
        )
    ''')
    print('Tabela criada.')
 
## INSERT DE DADOS NAS TABELAS
with sqlite3.connect('pipeline.db') as conn:
    conn.execute('''
        INSERT INTO documentos (nome, origem, status, num_tokens)
        VALUES (?, ?, ?, ?)
    ''', ('documento1.txt', 'upload', 'pendente', 100))
    print('Registro inserido.')


## INSERT EM LOTE
with sqlite3.connect('pipeline.db') as conn:
    registros = [
        ('documento2.txt', 'upload', 'pendente', 200),
        ('documento3.txt', 'upload', 'pendente', 300),
        ('documento4.txt', 'upload', 'pendente', 400),
    ]
    conn.executemany('''
        INSERT INTO documentos (nome, origem, status, num_tokens)
        VALUES (?, ?, ?, ?)
    ''', registros)
    print('Registros em lote inseridos.')
    
## CONSULTA DE DADOS
with sqlite3.connect('pipeline.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documentos')
    registros = cursor.fetchall()
    print(registros)
        
## CONSULTA DE DADOS COM FILTRO
with sqlite3.connect('pipeline.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documentos WHERE status = ?', ('pendente',))
    registros = cursor.fetchall()
    print(registros)
    
## CRIAR RELACIONAMENTO ENTRE TABELAS
with sqlite3.connect('pipeline.db') as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            documento_id INTEGER NOT NULL,
            token       TEXT    NOT NULL,
            criado_em   TEXT    DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (documento_id) REFERENCES documentos(id)
        )
    ''')
    tokens = [
        (1, 'token1'),
        (1, 'token2'),
        (2, 'token3'),
        (2, 'token4'),
        (3, 'token5'),
    ]
    conn.executemany('''
        INSERT INTO tokens (documento_id, token)
        VALUES (?, ?)
    ''', tokens)
    print('Tablela de tokens criada e populada.')
    