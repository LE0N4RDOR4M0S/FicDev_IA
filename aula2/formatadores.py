# Formatações do numero de casas decimais
pi = 3.141592653589793
print(f"{pi:.2f}")  # 2 casas decimais
print(f"{pi:.6f}")  # 6 casas decimais

# Separador de milhar
print(f"{pi*10000:,.2f}")

# Alinhamento
print(f"{pi:<0.2f} <- Alinhado a esquerda")
print(f"{pi:^10.2f} <- Centralizado")
print(f"{pi:>10.2f} <- Alinhado a direita")