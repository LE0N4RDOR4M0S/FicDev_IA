from calculo import media, aprovado

def main():
    alunos = [
        {"nome": "Alice", "notas": [10.0, 8.5, 7.0]},
        {"nome": "Bob", "notas": [6.5, 7.0, 8.0]},
        {"nome": "Charlie", "notas": [9.0, 8.5, 7.5]}
    ]
    
    for aluno in alunos:
        print(f"{aluno['nome']}")
        print(f"Média final: {media(aluno['notas']):.2f}")
        print(f"Aprovado: {'Sim' if aprovado(media(aluno['notas'])) else 'Não'}")
        print("-" * 50)
        
main()