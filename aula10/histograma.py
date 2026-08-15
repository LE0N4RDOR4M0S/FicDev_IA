import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
notas_turma = np.concatenate([
    np.random.normal(loc=7.5, scale=1.2, size=70),  # maioria no meio
    np.random.uniform(low=3.0, high=5.0, size=20),   # alunos com dificuldade
])
notas_turma = np.clip(notas_turma, 0, 10)  # limitar entre 0 e 10

fig, ax = plt.subplots(figsize=(9, 5))

n, bins, patches = ax.hist(
    notas_turma,
        bins=15,              # número de intervalos
        color='#2E86C1',
        edgecolor='white',
        linewidth=0.8,
        alpha=0.85            # leve transparência
)

for patch, left_edge in zip(patches, bins[:-1]):
    if left_edge < 7.0:
        patch.set_facecolor('#E74C3C')

media = notas_turma.mean()
ax.axvline(x=media, color='red', linestyle='--', linewidth=2, label=f'Média: {media:.2f}')

ax.axvline(x=7.0, color='gray', linestyle=':', linewidth=1.5, label='Mínimo aprovação (7.0)')

ax.set_xlabel('Nota Final')
ax.set_ylabel('Número de Alunos')
ax.legend()

plt.tight_layout()
plt.savefig('histograma_notas.pdf', dpi=300, bbox_inches='tight')
plt.show()