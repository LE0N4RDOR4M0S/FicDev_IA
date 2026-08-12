from __future__ import annotations

from collections.abc import Iterable


def validar_notas(notas: Iterable[float]) -> list[float]:
    notas_validadas = []

    for nota in notas:
        if not isinstance(nota, (int, float)):
            raise ValueError("Todas as notas devem ser numéricas.")

        nota_formatada = float(nota)
        if nota_formatada < 0 or nota_formatada > 10:
            raise ValueError("As notas devem estar entre 0 e 10.")

        notas_validadas.append(nota_formatada)

    if not notas_validadas:
        raise ValueError("Informe ao menos uma nota.")

    return notas_validadas
