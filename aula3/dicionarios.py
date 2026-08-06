# Estrutura de dados representada com coleções de elementos, como listas, tuplas, dicionários e sets.
# Armazena informações por chave-valor, índice ou posição, dependendo do tipo de coleção.
# Chaves literais
aluno = {
    'nome': 'Ana Silva',
    'idade': 20,
    'notas': [8.5, 9.0, 7.5],
    'ativo': True
}

# Acesso feito via chave, se a chave não existir, gera KeyError
print(aluno['nome']) # Ana Silva
print(aluno['idade']) # 20
print(aluno['notas']) # [8.5, 9.0, 7.5]
print(aluno['ativo']) # True

# .get() - Opção de acesso que não gera erro caso a chave não exista.
print(aluno.get('nome')) # Ana Silva
print(aluno.get('endereco')) # None

# Remover elementos
email = aluno.pop('email', None) # Remove a chave 'email' e retorna o valor, se não existir retorna None
print(email) # None

# Adicionar e atualizar elementos
aluno['email'] = 'ana@email.com'
aluno['idade'] = 21

print(aluno)

# Verificar se uma chave existe
print('nome' in aluno) # True
print('endereco' in aluno) # False

# Iterar sobre chaves, valores ou itens (chave-valor)
for chave in aluno:
    print(chave, aluno[chave])

# Iterar sobre valores
for chave in aluno.values():
    print(chave)

# Iterar sobre pares chave-valor
for chave, valor in aluno.items():
    print(f"{chave}: {valor}")
    
print('#'*50)
#############################################################
# Estrutura típica de API/ banco de dados
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

# Como navegar em estruturas aninhadas
print(turma['nome']) # Turma A - Python para IA
print(turma['alunos'][0]['nome']) # Ana Silva
print(turma['alunos'][1]['notas'][0]) # 6.5
print(turma['alunos'][2]['ativo']) # True

# Calcular média de cada aluno
for aluno in turma['alunos']:
    media = sum(aluno['notas']) / len(aluno['notas'])
    print(f"{aluno['nome']} - Média: {media:.2f}")
