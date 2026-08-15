import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['figure.dpi']      = 120       # resolução da figura
plt.rcParams['font.family']     = 'sans-serif'
plt.rcParams['axes.spines.top']    = False   # remove borda superior
plt.rcParams['axes.spines.right']  = False   # remove borda direita


fig, ax = plt.subplots(figsize=(8,5))
ax.plot([1, 2, 3, 4], [10, 20, 15, 30])
ax.set_title('Hello World')
ax.set_xlabel('Período')
ax.set_ylabel('Valor')

plt.tight_layout()
plt.savefig('grafico.png', dpi=150, bbox_inches='tight')
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))


# Dados: evolução das médias da turma por bimestre
bimestres = ['1º Bim', '2º Bim', '3º Bim', '4º Bim']
media_turma_a = [7.2, 7.5, 6.8, 8.1]
media_turma_b = [6.5, 7.0, 7.3, 7.8]


fig, ax = plt.subplots(figsize=(9,5))
ax.plot(bimestres, media_turma_a, marker='o', label='Turma A', color='#2E86C1', linewidth=2)
ax.plot(bimestres, media_turma_b, marker='o', label='Turma B', color='#E74C3C', linewidth=2)
ax.axhline(y=7.0, color='gray', linestyle=':', linewidth=1.5, label='Mínimo aprovação (7.0)')
ax.set_title('Evolução da média por bimestre', fontsize=14, fontweight='bold')
ax.set_xlabel('Bimestre')
ax.set_ylabel('Média por turma')
ax.set_ylim(5.0, 10.0)
ax.legend()
ax.grid(axis='y', alpha=0.4)

plt.tight_layout()
plt.savefig('grafico_linhas.png', dpi=150, bbox_inches='tight')
plt.show()

# gráfico de barras

disciplinas = ['Matemática', 'Português', 'História', 'Ciências', 'Inglês']
medias = [7.3, 8.1, 7.8, 6.9, 8.4]
cores  = ['#2E86C1' if m >= 7.0 else '#E74C3C' for m in medias]

fig, ax = plt.subplots(figsize=(9, 5))

barras = ax.bar(disciplinas, medias, color=cores,
                width=0.6, edgecolor='white', linewidth=0.8)

for barra in barras:
    altura = barra.get_height()
    ax.text(
        barra.get_x() + barra.get_width() / 2,  # posição x: centro da barra
        altura + 0.05,                           # posição y: levemente acima
        f'{altura:.1f}',                         # texto: valor formatado
        ha='center', va='bottom', fontsize=10, fontweight='bold'
    )

ax.axhline(y=7.0, color='gray', linestyle='--', linewidth=1.2,
           label='Mínimo aprovação')
ax.set_title('Média por Disciplina — Todas as Turmas', fontsize=14, fontweight='bold')
ax.set_ylabel('Média')
ax.set_ylim(0, 10)
ax.legend()

plt.tight_layout()
plt.savefig('grafico_barras.png', dpi=150, bbox_inches='tight')
plt.show()

turmas      = ['Turma A', 'Turma B', 'Turma C']
aprovados   = [28, 22, 30]
reprovados  = [2, 8, 0]


x = range(len(turmas))  # posições no eixo x
largura = 0.35

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar([i - largura/2 for i in x], aprovados, largura, label='Aprovados', color='#27AE60')
ax.bar([i + largura/2 for i in x], reprovados, largura, label='Reprovados', color='#E74C3C')

ax.set_xticks(x)
ax.set_xticklabels(turmas)
ax.set_title('Resultado por Turma', fontsize=14, fontweight='bold')
ax.set_ylabel('Número de Alunos')
ax.legend()
ax.set_ylim(0, 35)

plt.tight_layout()
plt.savefig('grafico_barras_vertical.png', dpi=150, bbox_inches='tight')
plt.show()

