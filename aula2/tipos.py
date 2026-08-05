nome = input("Qual o seu nome?\n")
print(f"Bem vindo, {nome}!")

print("-"*40)

idade = input("Qual a sua idade?\n")
salario = input("Qual o seu salário?\n")
print(f"Você tem {idade} anos e recebe R${salario}.")

cidade = input("Qual a sua cidade?\n")
print(f"Você mora em {cidade}.")

peso = input("Qual o seu peso?\n")
altura = input("Qual a sua altura?\n")
imc = float(peso) / (float(altura) ** 2)
print(f"Seu IMC é {imc}.")