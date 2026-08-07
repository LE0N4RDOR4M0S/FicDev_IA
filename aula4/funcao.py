# Uma função no python são blocos nomeados de código que recebem parametros e retornam valores.


# palavra reservada "def" seguida do nome da função
def saudar(nome):
    return f"Olá, {nome}!"

# Isso previnirá que o código seja executado várias vezes, sendo necessário mudar apenas o parametro
print(saudar('Ana'))
print(saudar('João'))
print(saudar('Maria'))

print("#"*60)

# Parametros e argumentos
def area_retangulo(base, altura):
    return base * altura

print(area_retangulo(5, 10))


# Parametro com valor padrão
def desconto(preco,
             percentual=10):
    return preco * (1 - percentual / 100)

print(desconto(100)) # Aqui a saida é 90
print(desconto(100, 20)) # Aqui a saida é 80, pois o valor do parametro percentual foi alterado para 20

print("#"*60)

# Passando parametros pelo nome (keyword arguments) (Não precisa estar ordenados)
def criar_perfil(nome, idade, cidade):
    return f"Nome: {nome}, Idade: {idade}, Cidade: {cidade}"

print(criar_perfil(nome='Ana', cidade='São Paulo', idade=25))

print("#"*60)

# args e kwargs
# São utilizados para passar uma quantidade não definida de parametros
# Args são posicionais (tuplas) e kwargs são nomeados (dicionários)
def somar(*args):
    return sum(args)

print(somar(1, 2, 3, 4, 5)) # Aqui a saida é 15

def cadastrar_usuario(**kwargs):
    return kwargs

print(cadastrar_usuario(nome='Ana', idade=25, cidade='São Paulo', qualquer_coisa='exemplo'))

print("#"*60)

# Retorno de funções
# Podem ser simples, com um valor ou complexos, com múltiplos valores (tuplas, listas, dicionários, etc)
def calcular_media(notas):
    """Calcular a média de uma lista de notas passada
    
    Args:
        notas (int): Lista de notas tiradas.
        
    Returns:
        float: Média das notas calculadas por soma(notas) / numero de notas
        
    Examples:
        >>> calcular_media([8, 9, 7, 6, 5, 0, 1, 10, 9])
        5.555555555555
        >>> calcular_media([1, 9])
        5.0 
    """
    
    if not notas:
        return 0.0
    return sum(notas) / len(notas)

print(calcular_media([8, 9, 7, 6, 5, 0, 1, 10, 9]))

def calcular_maior_menor_nota(notas):
    if not notas:
        return None, None
    return max(notas), min(notas)

maior, menor = calcular_maior_menor_nota([8, 9, 7, 6, 5, 0, 1, 10, 9])
print(f"Maior nota: {maior}, Menor nota: {menor}")

# Funções com return None podem ser declaradas sem o return

def separador(c = '#', tam = 60):
    print(c * tam)
    
separador()
separador(tam = 10)
separador(c = '-', tam = 20)

result = separador()
print(result) # Aqui a saida é None, pois a função não retorna nada
print(separador()) # Aqui a saida é None, pois a função não retorna nada