import numpy as np

a = np.array([[0.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

print(a)
print(a.shape)
print(a.ndim)
print(a.size)
print(a.dtype)
print("#"*50)


# Determinar o tipo na criação
f32 = np.array(a, dtype=np.bool)
print(f32.dtype)
print(f32)
print("#"*50)

# Convertendo o tipo
inteiros = a.astype(np.int32)
print(inteiros.dtype)
print(inteiros)
print(a.nbytes)
print(f32.nbytes)
