temperatura = 25

if temperatura >= 35:
    print("Está quente")
elif temperatura >= 25:
    print("Está agradável")
elif temperatura >= 15:
    print("Está fresco")
else:
    print("Está frio")
    
    
print("-"*50)
media = 6.0
presenca = 0.74

if media >= 7.0 and presenca >= 0.75:
    print("Aprovado")
elif media < 7.0 and presenca < 0.75:
    print("Reprovado por média e presença")
elif presenca < 0.75:
    print("Reprovado por presença")
else:
    print("Reprovado por média")
    
print("-"*50)

idade = 17
status = "De maior" if idade >= 18 else "De menor"
print(status)