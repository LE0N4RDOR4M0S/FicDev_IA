import pdfplumber
import pandas as pd

with pdfplumber.open('83800_por.pdf') as pdf:
    pagina = pdf.pages[0]

    tabela = pagina.extract_table()
    if tabela:
        df = pd.DataFrame(tabela[1:], columns=tabela[0])
        print(df)

    tabelas = pagina.extract_tables()
    print(f'{len(tabelas)} tabela(s) na página 1')

    for i, pag in enumerate(pdf.pages):
        for j, tabela in enumerate(pag.extract_tables()):
            df = pd.DataFrame(tabela[1:], columns=tabela[0])
            df.to_csv(f'tabela_p{i+1}_t{j+1}.csv', index=False)
            print(f'Tabela {j+1} da página {i+1}: {df.shape}')