import pandas as pd

df = pd.DataFrame({
    'aluno':    ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena'],
    'turma':    ['A', 'B', 'A', 'C', 'B'],
    'situacao': ['Aprovado', 'Reprovado', 'Aprovado', 'Aprovado', 'Reprovado'],
    'media':    [8.5, 5.5, 7.8, 7.2, 6.0],
    'faltas':   [2, 10, 3, 1, 8] 
})

df_encoded = pd.get_dummies(df, columns=['turma'], prefix='turma', dtype=int)
print(df_encoded.columns.tolist())

df_encoded['situacao_num'] = df_encoded['situacao'].map({'Aprovado': 1, 'Reprovado': 0})

df_encoded = df_encoded.drop(columns=['situacao', 'aluno'])
print(df_encoded)

# Normalização de escalas
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split

scaler_std = StandardScaler()

colunas_numericas = ['media', 'faltas']

df_scaled = df_encoded.copy()
df_scaled[colunas_numericas] = scaler_std.fit_trwansform(
    df_encoded[colunas_numericas]
)
print(df_scaled[colunas_numericas].describe())

scaler_mm = MinMaxScaler()
df_minmax = df_encoded.copy()
df_minmax[colunas_numericas] = scaler_mm.fit_transform(
    df_encoded[colunas_numericas]
)
print(df_minmax[colunas_numericas].describe())

x =  df_scaled.drop(columns=['situacao_num'])
y = df_scaled['situacao_num']

X_treino, X_teste, y_treino, y_teste = train_test_split(
    x, y, 
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Tamanho do conjunto de treino:", len(X_treino))
print("Tamanho do conjunto de teste:", len(X_teste))

X_treino.to_csv('X_treino.csv', index=False)
X_teste.to_csv('X_teste.csv', index=False)
y_treino.to_csv('y_treino.csv', index=False)
y_teste.to_csv('y_teste.csv', index=False)