import sys
from pathlib import Path

from analise.relatorio import gerar_relatorio_turma


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python -m analise caminho/do/turma.json [caminho/do/relatorio.csv]")
        sys.exit(1)

    caminho_json = Path(sys.argv[1])
    caminho_csv = Path(sys.argv[2]) if len(sys.argv) > 2 else caminho_json.with_name("relatorio.csv")

    if not caminho_json.exists():
        print(f"Erro: arquivo não encontrado: {caminho_json}")
        sys.exit(1)

    try:
        resultado = gerar_relatorio_turma(caminho_json, caminho_csv)
    except ValueError as erro:
        print(f"Erro: {erro}")
        sys.exit(1)

    print(f"Relatório gerado em: {resultado['arquivo_saida']}")
    print(f"Alunos processados: {resultado['total_alunos']}")


if __name__ == "__main__":
    main()
