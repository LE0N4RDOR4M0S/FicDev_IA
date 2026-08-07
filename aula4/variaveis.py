# O escopo define onde uma variavel pode ser acessada
# No python, temos dois tipos de escopo: local e global
# Locais: existem dentro de funções e não podem ser acessadas fora delas
# Globais: existem fora de funções e podem ser acessadas dentro delas

taxa_de_juros = 0.05 # Variavel global

def calcular_juros(valor, meses):
    juros = valor * taxa_de_juros * meses
    return juros

print(calcular_juros(1000, 12))
#print(juros) # Aqui vai dar erro, pois a variavel juros é local e não pode ser acessada fora da função

# Não é uma boa prática alterar variaveis globais dentro de funções, mas é possível fazer isso utilizando a palavra reservada global
def alterar_taxa_de_juros(nova_taxa):
    global taxa_de_juros
    taxa_de_juros = nova_taxa
    
print(taxa_de_juros)
alterar_taxa_de_juros(0.1)
print(taxa_de_juros)