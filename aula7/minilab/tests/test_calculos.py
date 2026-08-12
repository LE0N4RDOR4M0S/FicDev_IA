import csv
import json

import pytest

from analise import aprovado, media, validar_notas
from analise.relatorio import gerar_relatorio_turma


def test_media_calcula_valor_correto() -> None:
    assert media([7, 8, 9]) == pytest.approx(8.0)


def test_aprovado_usa_media_minima() -> None:
    assert aprovado(6.0) is True
    assert aprovado(5.99) is False


def test_validar_notas_rejeita_lista_vazia() -> None:
    with pytest.raises(ValueError):
        validar_notas([])


def test_gerar_relatorio_turma_cria_csv_com_todos_os_alunos(tmp_path) -> None:
    caminho_json = tmp_path / "turma.json"
    caminho_csv = tmp_path / "relatorio.csv"

    caminho_json.write_text(
        json.dumps(
            {
                "turma": "Turma de teste",
                "nota_aprovacao": 7.0,
                "alunos": [
                    {"id": 1, "nome": "Ana", "curso": "Dados", "notas": [8.5, 9.0, 7.5]},
                    {"id": 2, "nome": "Bruno", "curso": "Dados", "notas": [5.5, 6.0, 7.0]},
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultado = gerar_relatorio_turma(caminho_json, caminho_csv)

    assert resultado["total_alunos"] == 2
    assert caminho_csv.exists()

    with caminho_csv.open(encoding="utf-8", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))

    assert linhas == [
        {"id": "1", "nome": "Ana", "curso": "Dados", "notas": "8.50;9.00;7.50", "media": "8.33", "situacao": "Aprovado"},
        {"id": "2", "nome": "Bruno", "curso": "Dados", "notas": "5.50;6.00;7.00", "media": "6.17", "situacao": "Reprovado"},
    ]
