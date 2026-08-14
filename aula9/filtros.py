import pandas as pd
df = pd.read_csv('vendas.csv', sep=';')
filtro = (df['Valor'] > 1000) & (df['Vendedor'] == 'Carlos')
df_filtrado = df[filtro]
print(df_filtrado)