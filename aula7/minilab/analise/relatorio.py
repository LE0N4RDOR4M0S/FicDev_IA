from __future__ import annotations

import json
from csv import DictWriter
from pathlib import Path

from .calculos import aprovado, media
from .validacao import validar_notas


def gerar_relatorio_turma(
    caminho_entrada: str | Path,
    arquivo_saida: str | Path | None = None,
) -> dict[str, object]:
    caminho_json = Path(caminho_entrada)
    if not caminho_json.exists():
        raise ValueError(f"arquivo não encontrado: {caminho_json}")

    with caminho_json.open(encoding="utf-8") as arquivo:
        dados_turma = json.load(arquivo)

    if not isinstance(dados_turma, dict):
        raise ValueError("o JSON da turma deve conter um objeto no nível raiz.")

    alunos = dados_turma.get("alunos")
    if not isinstance(alunos, list) or not alunos:
        raise ValueError("o JSON da turma deve conter uma lista de alunos.")

    limite_aprovacao = float(dados_turma.get("nota_aprovacao", 6.0))
    caminho_csv = Path(arquivo_saida) if arquivo_saida is not None else caminho_json.with_name("relatorio.csv")
    caminho_csv.parent.mkdir(parents=True, exist_ok=True)

    linhas_relatorio: list[dict[str, object]] = []
    with caminho_csv.open("w", newline="", encoding="utf-8") as arquivo:
        gravador = DictWriter(arquivo, fieldnames=["id", "nome", "curso", "notas", "media", "situacao"])
        gravador.writeheader()

        for aluno in alunos:
            if not isinstance(aluno, dict):
                raise ValueError("cada aluno deve ser um objeto JSON válido.")

            notas_validadas = validar_notas(aluno.get("notas", []))
            media_final = media(notas_validadas)
            situacao = "Aprovado" if aprovado(media_final, limite_aprovacao) else "Reprovado"

            linha = {
                "id": aluno.get("id", ""),
                "nome": aluno.get("nome", ""),
                "curso": aluno.get("curso", ""),
                "notas": ";".join(f"{nota:.2f}" for nota in notas_validadas),
                "media": f"{media_final:.2f}",
                "situacao": situacao,
            }
            linhas_relatorio.append(linha)
            gravador.writerow(linha)

    return {
        "turma": dados_turma.get("turma", ""),
        "total_alunos": len(linhas_relatorio),
        "arquivo_saida": str(caminho_csv),
        "alunos": linhas_relatorio,
    }
