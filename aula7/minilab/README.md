# Análise de Notas

Projeto em Python para validar notas de alunos, calcular a média e informar se o aluno foi aprovado.

## Como instalar

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Como usar

Execute o pacote pela linha de comando informando o caminho do JSON da turma:

```bash
python -m analise data/turma.json
```

O programa lê todos os alunos do JSON, calcula a média de cada um e gera o arquivo `data/relatorio.csv`.

Se quiser escolher outro destino para o CSV, passe um segundo argumento:

```bash
python -m analise data/turma.json saida/relatorio.csv
```

## Testes

```bash
pytest
```
