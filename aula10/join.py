import pandas as pd


cadastro = pd.DataFrame({
    'id_aluno': [1, 2, 3, 4, 5],
    'nome':     ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena'],
    'turma':    ['A', 'A', 'B', 'B', 'C'],
})

notas = pd.DataFrame({
    'id_aluno':  [1, 2, 3, 4, 6],   # aluno 5 ausente, aluno 6 extra
    'matematica': [8.5, 7.0, 9.0, 5.5, 8.0],
    'portugues':  [7.5, 8.5, 6.0, 7.0, 9.5],
})


# inner join
print("\nINNER JOIN")
df_innner = pd.merge(cadastro, notas , on='id_aluno', how='inner')
print(df_innner)

# left join
print("\nLEFT JOIN")
df_left = pd.merge(cadastro, notas , on='id_aluno', how='left')
print(df_left)

# OUTER JOIN
print("\nOUTER JOIN")
df_outer = pd.merge(cadastro, notas , on='id_aluno', how='outer')
print(df_outer)

frequencias = pd.DataFrame({
    'matricula': [1, 2, 3, 4, 5],   # mesmo significado que 'id_aluno'
    'faltas':    [2, 0, 5, 1, 3],
})

print("\nFREQUENCIAS")
print(frequencias)

# Para usar colunas com nomes diferentes
df_completo = pd.merge(cadastro, frequencias, left_on='id_aluno', right_on='matricula', how='left')

print("\nJOIN COM NOMES DIFERENTES")
print(df_completo)

df_final = (cadastro.merge(notas, on='id_aluno', how='left').merge(frequencias, left_on='id_aluno', right_on='matricula', how='left')).drop(columns='matricula')

print("\nFINAL")
print(df_final)

print(df_final.isnull().sum())

print("##"*50)
avaliacoes = pd.DataFrame({
    'aluno':      ['Ana','Ana','Ana','Bruno','Bruno','Bruno'],
    'disciplina': ['Mat','Port','Hist','Mat','Port','Hist'],
    'nota':       [8.5, 7.5, 9.0, 7.0, 8.5, 6.5],
})

print(avaliacoes)
tabela_larga = avaliacoes.pivot_table(values='nota', index='aluno', columns='disciplina')
print(tabela_larga)
tabela_larga = tabela_larga.reset_index()
print(tabela_larga)
tabela_larga.columns.name = None
print(tabela_larga)

# Formato longo
print("\nFORMATO LONGO")
notas_largas = pd.DataFrame({
    'aluno':      ['Ana', 'Bruno', 'Carla'],
    'matematica': [8.5,   7.0,    9.0],
    'portugues':  [7.5,   8.5,    6.0],
    'historia':   [9.0,   6.5,    8.0],
})

notas_longas = notas_largas.melt(
    id_vars='aluno',
    var_name='disciplina',
    value_name='nota'
)
print(notas_longas)