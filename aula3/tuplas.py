# Criação de tuplas
coordenadas = (23.5, -46.6)
rgb_vermelho = (255, 0, 0)
versao = (3, 14, 4)
notas = (7.5, 8.0, 9.2)
unitaria = (42,) # Para tupla de um elemento, é necessário a vírgula

# Existem tuplas sem parênteses
sem_paren = 'a', 'b', 'c'
print(type(sem_paren)) # <class 'tuple'>

# Acesso: idêntico às listas
print(coordenadas[0])
print(versao[-1])
print(notas[0:3])

# Desempacotamento de tuplas
lat, lon = coordenadas
print(f"Latitude: {lat}, Longitude: {lon}")
maior, meio, menor = sorted(notas, reverse=True)
print(f"Maior: {maior}, Meio: {meio}, Menor: {menor}")

# Desempacotamento com *
primeiro, *resto = (1, 2, 3, 4, 5)
print(primeiro)
print(resto)

# Tupla como chave de dicionário
distancias = {
    ('São Paulo', 'Rio de Janeiro'): 429,
    ('São Paulo', 'Belo Horizonte'): 586,
}

# Funções retornando múltiplos valores (retornam tupla)
def min_max(lista):
    return min(lista), max(lista)

minimo, maximo = min_max(notas)
print(f"Mínimo: {minimo}, Máximo: {maximo}")

# Qualquer tentativa de alterar elementos de uma tupla
# resulta em erro, são imutáveis

# Não é possível deletar elementos, porém é possível
# deletar a tupla inteira
del coordenadas