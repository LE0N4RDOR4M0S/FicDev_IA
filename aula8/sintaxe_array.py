import numpy as np

a = np.array([10, 20, 30, 40, 50, 60])

# Indexação simples
print("Indexação simples")
print(a[0])
print(a[1])
print(a[-1])
print("#"*50)

print("\nIndexação com fatiamento")
print(a[1:4])
print(a[:3])
print(a[3:])
print(a[::2])
print(a[::-1])
print("#"*50)

## Se a fatia for modificada, o array original também será modificado
print("\nModificando a fatia, modificando o array original")
fatia = a[1:5]
fatia[0] = 999
print(a)
print(fatia)
print("#"*50)

copia = a[1:5].copy()
copia[0] = 0
print(a)
print(copia)

## Arrays 2D

m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(m[0,0])
print(m[1,2])
print(m[-1,-1])

# Seleciona uma linha inteira
print(m[0])
print(m[1,:])
print(m[-1,:])

#Selecionar uma coluna inteira
print(m[:,0])
print(m[:,1])

