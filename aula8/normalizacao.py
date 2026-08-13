import numpy as np

dados = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9]], dtype=np.float32)

x_min = dados.min(axis=0)
x_max = dados.max(axis=0)

print("Mínimos por coluna:", x_min)
print("Máximos por coluna:", x_max)

dados_normalizados = (dados - x_min) / (x_max - x_min)
print(dados_normalizados)

print(dados_normalizados.min())
print(dados_normalizados.max())

def normalizar_minmax(arr: np.ndarray) -> np.ndarray:
    """
    Normaliza um array para o intervalo[0,1].
    Args:
        arr: Array NumPy com os dados originais.
        
    Returns:
        Array NumPy com os dados normalizado no intervalo[0,1].
    """
    x_min = arr.min()
    x_max = arr.max()
    
    
    if x_max == x_min:
        return np.zeros_like(arr, dtype=float)
    return (arr - x_min) / (x_max - x_min)

matriz = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float32)
col_min = matriz.min(axis=0)
col_max = matriz.max(axis=0)
normalizada = (matriz - col_min) / (col_max - col_min)
print(normalizada)  