import numpy as np

m = np.ones((3, 4))
v = np.array([1, 2, 3, 4])

print((m+v).shape)
print(m+v)

col = np.array([[1], [2], [3]])
lin = np.array([[10, 20, 30, 40]])
print((col + lin).shape)

dados = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float32)
print(dados)

medias = dados.mean(axis=0)
print(medias)

centralizado = dados - medias
print(centralizado)