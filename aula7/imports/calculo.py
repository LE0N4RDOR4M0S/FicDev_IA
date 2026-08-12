def media(notas: list[float]) -> float:
    if not notas:
        raise ValueError('Lista vazia')
    return sum(notas)/len(notas)

def aprovado(media: float, minimo: float = 7.0) -> bool:
    return media >= minimo