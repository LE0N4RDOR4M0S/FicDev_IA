import pandas as pd

df = pd.DataFrame({
    'nome': ['Alice', 'Bob', 'Charlie', 'David'],
    'turma': ['A', 'B', 'A', 'B'],
    'idade': [25, 30, 35, 40],
    'nota': [8.5, 7.0, 9.0, 6.5]
})

print(df)

df = pd.read_csv('vendas.csv',sep=';', decimal=',', encoding='utf-8', nrows=1000, usecols=['Data', 'Valor', 'Cliente'])

print(df)

# Excel
df = pd.read_excel('relatorio.xlsx', sheet_name='Jan_2024')

# Para extrair os nomes dos sheets das planilhas do Excel
xls = pd.ExcelFile('relatorio.xlsx')
df_final = pd.DataFrame()
print(xls.sheet_names)
df_final = pd.concat([pd.read_excel('relatorio.xlsx', sheet_name=sheet) for sheet in xls.sheet_names])
# for sheet in xls.sheet_names:
#     df = pd.read_excel('relatorio.xlsx', sheet_name=xls.sheet_names)
#     df_final = pd.concat([df_final, df], ignore_index=True)

print(df_final)
df_final.to_csv('resultado.csv', index=False, encoding='utf-8')
# Para exportar para Excel
df_final.to_excel('resultado.xlsx', index=False, sheet_name='Resultados')

# # Para adicionar uma nova aba em um arquivo Excel existente
# with pd.ExcelWriter('relatorio.xlsx', mode='a', engine='openpyxl') as writer:
#     df_final.to_excel(writer, index=False, sheet_name='Resultados')
    
print("#"*50)
print("Formatos")
print(df_final.shape)
print(df_final.info())
print(df_final.nunique())

print()