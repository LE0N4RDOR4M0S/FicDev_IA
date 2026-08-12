from analise import media, aprovado
 
notas_brutas = [8.5, 11.0, 9.0, -1.0, 7.5]
notas_limpas = [n for n in notas_brutas if 0 <= n <= 10]
print(f'Média: {media(notas_limpas):.2f}')


