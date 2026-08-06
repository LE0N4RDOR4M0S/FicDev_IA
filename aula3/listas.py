# Criação
notas = [7.5, 8.0, 9.2, 6.8, 10.0]
nomes = ['Ana', 'Bruno', 'Carla', 'Diego']
misto = [1, 'texto', 3.14, True, None] # heterogênea
vazia = []

# Acesso por índice (começa em 0)
print(notas[0]) # 7.5 (primeiro)
print(notas[-1]) # 10.0 (último)
print(notas[-2]) # 6.8 (penúltimo)

# Fatiamento (slicing): lista[inicio:fim:passo]
print(notas[1:3]) # [8.0, 9.2] — índices 1 e 2
print(notas[:3]) # [7.5, 8.0, 9.2] — do início até índice 2
print(notas[2:]) # [9.2, 6.8, 10.0] — do índice 2 até o fim
print(notas[::2]) # [7.5, 9.2, 10.0] — de 2 em 2
print(notas[::-1]) # [10.0, 6.8, 9.2, 8.0, 7.5] — invertida

# Métodos de uso

# Adicionar elementos
notas.append(8.5) # adiciona no final
print(notas)

# Insere em um indice específico
notas.insert(2, 7.8) # insere 7.8 no indice 2
print(notas)

# Adiciona vários no final
notas.extend([9.5, 6.0]) # adiciona 9.5 e 6.0 no final
print(notas)

# Remover elementos
notas.remove(6.8) # remove o valor 6.8
print(notas)

ultimo = notas.pop() # remove o último elemento e retorna ele
print(ultimo)

segundo = notas.pop(1) # remove o elemento do índice 1 e retorna ele
print(segundo)

del notas[0] # remove o elemento do índice 0 sem retornar
print(notas)

# Ordenação
notas.sort() # ordena do menor para o maior
print(notas)

notas.sort(reverse=True) # ordena do maior para o menor
print(notas)

ordenado = sorted(notas) # retorna uma nova lista ordenada
print(ordenado)

# Inverte a ordem dos elementos
notas.reverse() # inverte a ordem da lista

# copia da lista
copia = notas.copy()

# Limpa todos os elementos da lista
notas.clear()
print(notas) 

notas = [7.5, 8.0, 9.2, 6.8, 10.0]

# Eleva todas os elementos ao quadrado
quadrados = [n ** 2 for n in notas]
print(quadrados)

# Filtrar elementos maiores que 7
maiores_que_sete = [n for n in notas if n > 7]
print(maiores_que_sete)

# Filtrar e transformar: notas aprovadas sendo arredondadas
aprovadas_redondas = [round((n), 0) for n in notas if n >= 7.0]
print(aprovadas_redondas)

nomes = ['Ana Silva', 'Bruno Costa', 'Carla Lima']

# Iniciais de cada nome
iniciais = [nome.split()[0][0] for nome in nomes]
print(iniciais) # ['A', 'B', 'C']