# Set é uma coleção não ordenada de elementos únicos.
categorias = {'gato', 'cachorro', 'passaro', 'gato', 'peixe', 'cachorro'}
# A ordem dos elementos não é garantida, e elementos duplicados são automaticamente removidos.
print(categorias)

vazio = {} # Não é possível criar um set vazio com {} pois isso cria um dicionário.
print(type(vazio)) # <class 'dict'>
vazio = set() # Forma correta de criar um set vazio
print(type(vazio)) # <class 'set'>

tags_brutas = ['python', 'java', 'python', 'c++', 'java', 'javascript']
tags_unicas = set(tags_brutas) # Remove duplicatas
print(tags_unicas)

# Teste de pertencimento
print('python' in tags_unicas) # True
print('ruby' in tags_unicas) # False

tags_unicas.add('ruby') # Adiciona um elemento
print(tags_unicas)

tags_unicas.discard('c++') # Remove um elemento, se existir
print(tags_unicas)

tags_unicas.remove('java') # Remove um elemento, se existir, caso contrário gera KeyError
print(tags_unicas)

#Operações de conjuntos
a = {1, 2, 3, 4, 5, 6}
b = {4, 5, 6, 7, 8, 9}

print(a | b) # Representa a união dos conjuntos a e b
print(a & b) # Representa a interseção dos conjuntos a e b
print(a - b) # Representa a diferença entre os conjuntos a e b
print(a ^ b) # Representa a diferença simétrica entre os conjuntos a e b

# Subconjunto e superconjunto
print({1, 2}.issubset(a)) # True, {1, 2} é subconjunto de a
print(a.issuperset({1, 2})) # True, a é superconjunto de {1, 2}

# Nos sets, não existe indexing, slicing ou ordenação,
# pois são coleções não ordenadas.