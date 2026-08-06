import json

# Serialização: objeto Python -> JSON
turma = {
    'nome': 'Turma A - Python para IA',
    'semestre': '2025-1',
    'alunos': [
        {
            'nome': 'Ana Silva',
            'idade': 20,
            'notas': [8.5, 9.0, 7.5],
            'ativo': True
        },
        {
            'nome': 'Bruno Costa',
            'idade': 22,
            'notas': [6.5, 7.0, 8.0],
            'ativo': False
        },
        {
            'nome': 'Carla Lima',
            'idade': 19,
            'notas': [9.5, 8.0, 9.0],
            'ativo': True
        }
    ]
}

# O método dumps() converte o objeto Python em uma string json.
# indent adiciona a identação de 4 espaços para vizualização
# ensure_ascii=False permite que caracteres especiais sejam exibidos corretamente
json_str = json.dumps(turma, indent=4, ensure_ascii=False)

print(json_str)
print('#'*50)

# Desserialização: JSON -> objeto Python
json_recebido = '''
{
    "nome": "Turma A - Python para IA",
    "semestre": "2025-1",
    "alunos": [
        {
            "nome": "Ana Silva",
            "idade": 20,
            "notas": [
                8.5,
                9.0,
                7.5
            ],
            "ativo": true
        },
        {
            "nome": "Bruno Costa",
            "idade": 22,
            "notas": [
                6.5,
                7.0,
                8.0
            ],
            "ativo": false
        },
        {
            "nome": "Carla Lima",
            "idade": 19,
            "notas": [
                9.5,
                8.0,
                9.0
            ],
            "ativo": true
        }
    ]
}
'''

turma = json.loads(json_recebido)
print(type(turma))
print(turma['nome'])
print(turma['semestre'])

print('#'*50)

# Leitura e escrita de arquivos JSON
turma = {
    'nome': 'Turma A',
    'alunos': [
        {'id': 1, 'nome': 'Ana', 'notas': [8.5, 9.0, 7.5]},
        {'id': 2, 'nome': 'Bruno', 'notas': [6.0, 5.5, 7.0]},
    ]
}

# json.dump() — escreve direto no arquivo (sem 's' no final)
with open('turma.json', 'w', encoding='utf-8') as f:
    json.dump(turma, f, indent=2, ensure_ascii=False)

# ─── Ler JSON do disco ───────────────────────────────────────
# json.load() — lê diretamente do arquivo (sem 's' no final)
with open('turma.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

print(type(dados))
print(dados['nome'])
print(dados['alunos'][0]['nome'])