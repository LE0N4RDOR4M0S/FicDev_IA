import numpy as np
import pandas as pd


TOTAL_AULAS = 80


def conceito(media: float) -> str:
    if media >= 9.0:
        return "A"
    if media >= 7.0:
        return "B"
    if media >= 5.0:
        return "C"
    return "D"


def main() -> None:
    dados = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "nome": ["Ana", "Bruno", "Carla", "Diego", "Elena", "Fabio", "Gabi", "Hugo", "Ines", "Joao"],
        "turma": ["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"],
        "idade": [20, 22, 21, np.nan, 20, 23, 21, 22, 20, np.nan],
        "faltas": [1, 3, 0, 5, 2, 0, 4, 6, 1, 3],
        "nota_1b": [8.5, 6.0, 9.5, 4.0, 7.5, 9.0, 6.5, 3.5, 7.5, 6.0],
        "nota_2b": [9.0, np.nan, 10.0, 5.0, 8.0, 8.5, 7.0, 4.5, 8.0, np.nan],
        "nota_3b": [7.5, 7.0, 9.0, np.nan, 7.0, 9.5, 6.0, 4.0, 7.5, 5.5],
        "nota_4b": [8.0, 5.5, 9.8, 4.5, 7.5, 8.0, np.nan, 3.5, 8.0, 6.0],
    }

    df = pd.DataFrame(dados)

    print("=== Inspeção Inicial ===")
    print(f"Shape: {df.shape}")
    print(df.dtypes)
    print()
    print("Valores ausentes por coluna:")
    print(df.isna().sum())
    print()
    print(df.describe().round(2))
    print()

    df["idade"] = df.groupby("turma")["idade"].transform(lambda serie: serie.fillna(serie.median()))

    colunas_nota = ["nota_1b", "nota_2b", "nota_3b", "nota_4b"]
    for coluna in colunas_nota:
        media_aluno = df[colunas_nota].mean(axis=1)
        df[coluna] = df[coluna].fillna(media_aluno.round(2))

    df_validado = df.dropna()
    print("NaN restantes:", df.isna().sum().sum())
    print(f"Linhas após dropna(): {len(df_validado)}")
    print(df[["nome", "idade", "nota_2b", "nota_3b", "nota_4b"]].to_string(index=False))
    print()

    df["media_final"] = df[colunas_nota].mean(axis=1).round(2)
    df["presenca_pct"] = ((TOTAL_AULAS - df["faltas"]) / TOTAL_AULAS * 100).round(1)
    df["situacao"] = np.where(
        (df["media_final"] >= 7.0) & (df["presenca_pct"] >= 75.0),
        "Aprovado",
        "Reprovado",
    )
    df["conceito"] = df["media_final"].apply(conceito)

    df["nota_media_turma"] = df.groupby("turma")["media_final"].transform("mean").round(2)
    df["delta_turma"] = (df["media_final"] - df["nota_media_turma"]).round(2)

    aprovados = df[df["situacao"] == "Aprovado"]
    reprovados = df[df["situacao"] == "Reprovado"]
    alto_risco = df[(df["media_final"] < 7.0) & (df["faltas"] >= 3)]

    print("=== Resultado Individual ===")
    cols_exib = ["nome", "turma", "media_final", "presenca_pct", "situacao", "conceito"]
    print(df[cols_exib].sort_values("media_final", ascending=False).to_string(index=False))
    print(f"\nAprovados: {len(aprovados)} | Reprovados: {len(reprovados)}")
    print(f"Alto risco (media<7 E faltas>=3): {len(alto_risco)} aluno(s)")
    print(alto_risco[["nome", "turma", "media_final", "faltas"]].to_string(index=False))
    print()

    frequencia = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "freq_1b": [96, 92, 100, 89, 95, 100, 90, 85, 99, 94],
            "freq_2b": [98, 90, 100, 88, 96, 100, 89, 84, 98, 93],
            "freq_3b": [97, 91, 100, 87, 95, 100, 88, 83, 99, 92],
            "freq_4b": [96, 89, 100, 86, 94, 100, 87, 82, 98, 91],
        }
    )
    df = pd.concat([df, frequencia.drop(columns=["id"]),], axis=1)

    print("=== Frequência Bimestral ===")
    print(df[["nome", "freq_1b", "freq_2b", "freq_3b", "freq_4b"]].to_string(index=False))
    print()

    resumo_turma = (
        df.groupby("turma")
        .agg(
            n_alunos=("nome", "count"),
            media_turma=("media_final", "mean"),
            melhor_nota=("media_final", "max"),
            pior_nota=("media_final", "min"),
            total_faltas=("faltas", "sum"),
            aprovados=("situacao", lambda serie: (serie == "Aprovado").sum()),
        )
        .round(2)
        .reset_index()
    )
    resumo_turma["pct_aprovacao"] = (resumo_turma["aprovados"] / resumo_turma["n_alunos"] * 100).round(1)

    print("=== Resumo por Turma ===")
    print(resumo_turma.to_string(index=False))
    print()

    df.to_csv("alunos_tratados.csv", index=False, encoding="utf-8")
    resumo_turma.to_csv("resumo_turmas.csv", index=False, encoding="utf-8")

    with pd.ExcelWriter("alunos.xlsx") as writer:
        df.to_excel(writer, index=False, sheet_name="alunos")
        resumo_turma.to_excel(writer, index=False, sheet_name="resumo")

    print("Arquivos salvos:")
    print(" alunos_tratados.csv — dataset completo (10 alunos × 12 colunas)")
    print(" resumo_turmas.csv — resumo por turma (2 linhas × 8 colunas)")
    print(" alunos.xlsx — planilha com abas de alunos e resumo")


if __name__ == "__main__":
    main()
