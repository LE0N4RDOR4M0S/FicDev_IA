# Iteração direta

frutas = ['maçã', 'banana', 'laranja', 'uva']

for fruta in frutas:
    print(fruta)
    
# Iterando sobre string
for letra in 'Python':
    print(letra, end='\n')
    
# Iterando sobre dicionário (chaves por padrão)
config = {
    'modelo': 'gpt-4',
    'temperatura': 0.7, 
    'max_tokens': 1000
}

for chave, valor in config.items():
    print(f"{chave}: {valor}")
    
# break e continue
notas = [8.0, 9.5, 3.0, 7.0, 5.5]
for nota in notas:
    if nota < 5.0:
        print(f'Nota critica encontrada: {nota}. Interrompendo.')
        break
    if nota < 7.0:
        continue
    print(f'Nota aprovada: {nota}')
    
# else no for - executa se o loop terminou sem break
for nota in [8.0, 9.5, 7.0]:
    if nota < 5.0:
        break
else:
    print('Todas as notas são maiores que 5.0')