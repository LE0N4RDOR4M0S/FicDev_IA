from __future__ import annotations

from collections.abc import Iterable


def media(notas: Iterable[float]) -> float:
    notas_lista = list(notas)
    if not notas_lista:
        raise ValueError("Informe ao menos uma nota válida.")

    return sum(notas_lista) / len(notas_lista)


def aprovado(media_final: float, limite: float = 6.0) -> bool:
    return media_final >= limite
