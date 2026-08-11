import csv
import json
import logging
import re
from pathlib import Path

# =============================================================
# extrator.py - Pipeline: TXT -> regex -> CSV + JSON
# Trilha Python para IA - Aula 06
# Autor: Leonardo de Oliveira Ramos
# =============================================================
"""
Le um arquivo TXT com dados desestruturados, extrai CPFs,
telefones e e-mails com regex e salva os resultados em
CSV e JSON.
"""

BASE_DIR = Path(__file__).parent
ARQUIVO_ENTRADA = BASE_DIR / "contatos.txt"
PASTA_SAIDA = BASE_DIR / "saida"
ARQUIVO_CSV = PASTA_SAIDA / "contatos.csv"
ARQUIVO_JSON = PASTA_SAIDA / "contatos.json"
LOGGER = logging.getLogger(__name__)


def configurar_logging() -> None:
	logging.basicConfig(
		level=logging.INFO,
		format="%(levelname)s: %(message)s",
	)


def ler_entrada(caminho: Path) -> str:
	if not caminho.exists():
		raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")
	return caminho.read_text(encoding="utf-8")


def extrair_cpf(texto: str) -> str:
	padrao = re.compile(r"\b(?:\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})\b")
	encontrado = padrao.search(texto)
	return encontrado.group(0) if encontrado else ""


def extrair_telefones(texto: str) -> list[str]:
	padrao = re.compile(
		r"(?:\(\d{2}\)\s*9?\s*\d{4,5}-?\d{4}|\b\d{2}(?:\s|-)\d{4,5}-?\d{4}\b)"
	)
	encontrados = [item.strip() for item in padrao.findall(texto)]
	vistos = set()
	unicos = []
	for telefone in encontrados:
		if telefone not in vistos:
			vistos.add(telefone)
			unicos.append(telefone)
	return unicos


def extrair_emails(texto: str) -> list[str]:
	padrao = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
	encontrados = [item.strip().lower() for item in padrao.findall(texto)]
	vistos = set()
	unicos = []
	for email in encontrados:
		if email not in vistos:
			vistos.add(email)
			unicos.append(email)
	return unicos


def extrair_nome(registro: str) -> str:
	linhas = [linha.strip() for linha in registro.splitlines() if linha.strip()]
	return linhas[0] if linhas else ""


def formatar_cpf(cpf: str) -> str:
	digitos = re.sub(r"\D", "", cpf)
	if len(digitos) != 11:
		return cpf
	return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"


def formatar_telefone(telefone: str) -> str:
	digitos = re.sub(r"\D", "", telefone)

	if len(digitos) == 10:
		ddd = digitos[:2]
		numero = digitos[2:]
		return f"({ddd}) {numero[:4]}-{numero[4:]}"

	if len(digitos) == 11:
		ddd = digitos[:2]
		numero = digitos[2:]
		return f"({ddd}) {numero[:5]}-{numero[5:]}"

	return telefone


def remover_cabecalho_por_regex(texto: str) -> str:
	padrao_titulo = re.compile(r"(?im)^\s*relat[oó]rio[^\n]*$")
	padrao_data = re.compile(r"(?im)^\s*gerado\s+em:\s*[^\n]*$")
	padrao_primeiro_item = re.compile(r"(?m)^\s*\d+\.\s+")

	tem_titulo = bool(padrao_titulo.search(texto))
	tem_data = bool(padrao_data.search(texto))
	primeiro_item = padrao_primeiro_item.search(texto)

	if not primeiro_item:
		return texto

	if tem_titulo or tem_data:
		return texto[primeiro_item.start():]

	return texto


def extrair_contatos(texto: str) -> list[dict[str, object]]:
	texto_sem_cabecalho = remover_cabecalho_por_regex(texto)
	blocos = re.split(r"\n\s*\d+\.\s+", "\n" + texto_sem_cabecalho)
	registros = [bloco.strip() for bloco in blocos if bloco.strip()]

	contatos = []
	for registro in registros:
		nome = extrair_nome(registro)
		cpf = formatar_cpf(extrair_cpf(registro))
		telefones = [formatar_telefone(t) for t in extrair_telefones(registro)]

		# Evita que um CPF numerico seja salvo por engano como telefone.
		cpf_digitos = re.sub(r"\D", "", cpf)
		telefones = [
			telefone
			for telefone in telefones
			if re.sub(r"\D", "", telefone) != cpf_digitos
		]

		vistos = set()
		telefones_unicos = []
		for telefone in telefones:
			if telefone not in vistos:
				vistos.add(telefone)
				telefones_unicos.append(telefone)
		telefones = telefones_unicos

		emails = extrair_emails(registro)

		if not (nome or cpf or telefones or emails):
			continue

		contatos.append(
			{
				"nome": nome,
				"cpf": cpf,
				"telefones": telefones,
				"emails": emails,
			}
		)

	return contatos


def salvar_csv(contatos: list[dict[str, object]], caminho: Path) -> None:
	with caminho.open("w", newline="", encoding="utf-8") as arquivo_csv:
		escritor = csv.DictWriter(
			arquivo_csv,
			fieldnames=["nome", "cpf", "telefones", "emails"],
		)
		escritor.writeheader()
		for contato in contatos:
			escritor.writerow(
				{
					"nome": contato["nome"],
					"cpf": contato["cpf"],
					"telefones": " | ".join(contato["telefones"]),
					"emails": " | ".join(contato["emails"]),
				}
			)


def salvar_json(contatos: list[dict[str, object]], caminho: Path) -> None:
	with caminho.open("w", encoding="utf-8") as arquivo_json:
		json.dump(contatos, arquivo_json, ensure_ascii=False, indent=2)


def main() -> None:
	configurar_logging()
	PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

	texto = ler_entrada(ARQUIVO_ENTRADA)
	contatos = extrair_contatos(texto)

	salvar_csv(contatos, ARQUIVO_CSV)
	salvar_json(contatos, ARQUIVO_JSON)

	LOGGER.info(
		"Total de contatos extraidos: %s\nRegistros salvos em: %s e %s",
		len(contatos),
		ARQUIVO_CSV,
		ARQUIVO_JSON,
	)


if __name__ == "__main__":
	main()