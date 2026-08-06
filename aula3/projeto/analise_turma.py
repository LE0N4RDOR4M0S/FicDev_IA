import json
from pathlib import Path

ARQUIVO_JSON = 'turma.json'
ARQUIVO_RELATORIO = 'relatorio.json'


def carregar_dados(caminho: Path) -> dict:
    try: 
        with caminho.open('r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:   
        print(f"Erro: O arquivo {caminho} não foi encontrado.")
        return {}

def calcular_media(notas: list[float]) -> float:
    return sum(notas) / len(notas) if notas else 0.0


def montar_relatorio(dados: dict) -> dict:
    turma = dados['turma']
    professor = dados['professor']
    nota_aprovacao = float(dados['nota_aprovacao'])
    alunos = dados['alunos']

    resultados_alunos = []
    cursos_unicos = set()
    medias = []

    for aluno in alunos:
        media = calcular_media(aluno['notas'])
        medias.append(media)
        cursos_unicos.add(aluno['curso'])

        resultado = {
            'id': aluno['id'],
            'nome': aluno['nome'],
            'curso': aluno['curso'],
            'notas': aluno['notas'],
            'media': round(media, 2),
            'status': 'Aprovado' if media >= nota_aprovacao else 'Reprovado'
        }
        resultados_alunos.append(resultado)

    aprovados = [aluno for aluno in resultados_alunos if aluno['status'] == 'Aprovado']
    reprovados = [aluno for aluno in resultados_alunos if aluno['status'] == 'Reprovado']

    aprovados_ordenados = sorted(aprovados, key=lambda aluno: aluno['media'], reverse=True)
    reprovados_ordenados = sorted(reprovados, key=lambda aluno: aluno['media'])

    media_turma = round(sum(medias) / len(medias), 2) if medias else 0.0
    maior_media = round(max(medias), 2) if medias else 0.0
    menor_media = round(min(medias), 2) if medias else 0.0

    relatorio = {
        'turma': turma,
        'professor': professor,
        'nota_aprovacao': nota_aprovacao,
        'quantidade_alunos': len(alunos),
        'cursos': sorted(list(cursos_unicos)),
        'media_turma': media_turma,
        'maior_media': maior_media,
        'menor_media': menor_media,
        'aprovados': aprovados_ordenados,
        'reprovados': reprovados_ordenados,
        'quantidade_aprovados': len(aprovados_ordenados),
        'quantidade_reprovados': len(reprovados_ordenados)
    }

    return relatorio

def exibir_relatorio(relatorio: dict) -> None:
    print('=== Relatório da Turma ===')
    print(f"Turma: {relatorio['turma']}")
    print(f"Professor: {relatorio['professor']}")
    print(f"Nota de aprovação: {relatorio['nota_aprovacapo']}")
    print(f"Quantidade de alunos: {relatorio['quantidade_alunos']}")
    print(f"Cursos da turma: {', '.join(relatorio['cursos'])}")
    print(f"Média da turma: {relatorio['media_turma']:.2f}")
    print(f"Maior média: {relatorio['maior_media']:.2f}")
    print(f"Menor média: {relatorio['menor_media']:.2f}")
    print(f"Aprovados: {relatorio['quantidade_aprovados']}")
    print(f"Reprovados: {relatorio['quantidade_reprovados']}")
    print('\nAlunos aprovados:')
    for aluno in relatorio['aprovados']:
        print(f"- {aluno['id']}. {aluno['nome']} | Curso: {aluno['curso']} | Média: {aluno['media']:.2f}")
    print('\nAlunos reprovados:')
    for aluno in relatorio['reprovados']:
        print(f"- {aluno['id']}. {aluno['nome']} | Curso: {aluno['curso']} | Média: {aluno['media']:.2f}")


def exportar_relatorio(relatorio: dict, caminho: Path) -> None:
    try:
        with caminho.open('w', encoding='utf-8') as arquivo:
            json.dump(relatorio, arquivo, ensure_ascii=False, indent=2)
            arquivo.write('\n')
    except Exception as e:
        print(f"Erro ao exportar o relatório: {e}")


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    arquivo_entrada = base_dir / ARQUIVO_JSON
    arquivo_saida = base_dir / ARQUIVO_RELATORIO

    dados = carregar_dados(arquivo_entrada)
    relatorio = montar_relatorio(dados)
    exibir_relatorio(relatorio)
    exportar_relatorio(relatorio, arquivo_saida)
    print(f'\nRelatório exportado para: {arquivo_saida}')


if __name__ == '__main__':
    main()
