# Manipulação de Strings

# Remove espaços em branco do início e do fim da string
nome = "   João da Silva   "
print(nome.strip())

# Tudo em maiusculas
print(nome.upper().strip())

# Tudo em minusculas
print(nome.lower().strip())

# Substitui uma palavra por outra
print(nome.replace("João", "Maria").strip())

# Verifica se são digitos
print(nome.strip().isdigit())

# Verifica se são letras
print(nome.strip().isalpha())

# Divide a lista pelo separador
print(nome.strip().split("da"))

# Conta as ocorrências de um termo
print(nome.strip().count("a"))

# Deixa a primeira letra maiúscula
print(nome.strip().lower().capitalize())