import numpy as np

# Array 1D
a = np.array([1, 2, 3, 4, 5])
print(a)
print(type(a))
print("#"*50)

# Array 2D
m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(m)
print(type(m))
print("#"*50)

# Arrays preenchidos
print(np.zeros(5))
print(np.ones((3, 4)))
print(np.full((2, 3), 7))
print("#"*50)

# Sequencias
print(np.arange(0, 10, 2))
print(np.linspace(0, 1, 3))
print("#"*50)

# Aleatórios
print(np.random.rand(3, 4))
print(np.random.randn(3, 4))
print(np.random.randint(0, 10, size = (3, 3)))
print("#"*50)

# Semente para reprodutibilidade
np.random.seed(42)
print(np.random.rand(3))