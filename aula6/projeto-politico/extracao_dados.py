import argparse
import csv
import json
import time
import unicodedata
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


URL_PARLAMENTARES = "https://www.congressonacional.leg.br/parlamentares/em-exercicio"
SAIDA_PADRAO = "/saida/parlamentares_em_exercicio"


def _normaliza_casa(codigo_casa: str) -> str:
	mapa = {
		"CD": "Camara dos Deputados",
		"SF": "Senado Federal",
	}
	return mapa.get(codigo_casa.strip().upper(), codigo_casa.strip())


def _normaliza_chave(texto: str) -> str:
	texto = unicodedata.normalize("NFKD", texto)
	texto = "".join(c for c in texto if not unicodedata.combining(c))
	texto = texto.lower().strip()
	saida = []
	ultimo_underscore = False
	for char in texto:
		if char.isalnum():
			saida.append(char)
			ultimo_underscore = False
		else:
			if not ultimo_underscore:
				saida.append("_")
				ultimo_underscore = True
	return "".join(saida).strip("_")


def _inserir_em_dict(destino: dict[str, Any], chave: str, valor: str) -> None:
	if not chave or not valor:
		return

	if chave not in destino:
		destino[chave] = valor
		return

	valor_atual = destino[chave]
	if isinstance(valor_atual, list):
		if valor not in valor_atual:
			valor_atual.append(valor)
		return

	if valor_atual != valor:
		destino[chave] = [valor_atual, valor]


def _texto_limpo(tag: Any) -> str:
	if not tag:
		return ""
	return " ".join(tag.get_text(" ", strip=True).split())


def _extrair_metadados(soup: BeautifulSoup) -> dict[str, str]:
	metadados: dict[str, str] = {}
	for meta in soup.find_all("meta"):
		chave = meta.get("name") or meta.get("property") or meta.get("itemprop")
		valor = meta.get("content")
		if not chave or not valor:
			continue
		metadados[chave.strip()] = valor.strip()
	return metadados


def _extrair_campos_rotulo_valor(soup: BeautifulSoup) -> dict[str, Any]:
	campos: dict[str, Any] = {}

	for dl in soup.find_all("dl"):
		dts = dl.find_all("dt")
		dds = dl.find_all("dd")
		for dt, dd in zip(dts, dds):
			rotulo = _normaliza_chave(_texto_limpo(dt))
			valor = _texto_limpo(dd)
			_inserir_em_dict(campos, rotulo, valor)

	for tr in soup.find_all("tr"):
		th = tr.find("th")
		td = tr.find("td")
		if not th or not td:
			continue
		rotulo = _normaliza_chave(_texto_limpo(th))
		valor = _texto_limpo(td)
		_inserir_em_dict(campos, rotulo, valor)

	return campos


def extrair_dados_pagina_parlamentar(
	pagina_parlamentar: str, sessao: requests.Session, timeout: int = 30
) -> dict[str, Any]:
	if not pagina_parlamentar:
		return {"url": "", "erro": "pagina_parlamentar_vazia", "filtros": {}}

	try:
		resposta = sessao.get(pagina_parlamentar, timeout=timeout)
		resposta.raise_for_status()
	except requests.RequestException as erro:
		return {
			"url": pagina_parlamentar,
			"erro": str(erro),
			"filtros": {},
		}

	soup = BeautifulSoup(resposta.text, "html.parser")
	titulo = _texto_limpo(soup.find("title"))
	metadados = _extrair_metadados(soup)
	campos = _extrair_campos_rotulo_valor(soup)

	descricao = (
		metadados.get("description")
		or metadados.get("og:description")
		or metadados.get("twitter:description")
		or ""
	)
	foto = (
		metadados.get("og:image")
		or metadados.get("og:image:secure_url")
		or metadados.get("twitter:image")
		or metadados.get("image")
		or ""
	)

	filtros: dict[str, Any] = {
		"perfil_titulo": titulo,
		"perfil_descricao": descricao,
		"perfil_foto": foto,
	}

	for chave, valor in metadados.items():
		if chave.startswith("sf_"):
			filtros[chave] = valor

	for chave, valor in campos.items():
		filtros[chave] = valor

	return {
		"url": pagina_parlamentar,
		"erro": "",
		"dominio": "camara" if "camara.leg.br" in pagina_parlamentar else "senado",
		"titulo": titulo,
		"descricao": descricao,
		"foto": foto,
		"metadados": metadados,
		"campos_extraidos": campos,
		"filtros": filtros,
	}


def extrair_parlamentares_em_exercicio(url: str = URL_PARLAMENTARES) -> list[dict[str, Any]]:
	resposta = requests.get(url, timeout=30)
	resposta.raise_for_status()

	soup = BeautifulSoup(resposta.text, "html.parser")
	linhas = soup.select("table.parlamentares tbody tr")

	parlamentares: list[dict[str, Any]] = []

	for linha in linhas:
		colunas = linha.find_all("td")
		if len(colunas) < 4:
			continue

		nome = colunas[0].get_text(strip=True)
		partido = colunas[1].get_text(strip=True)
		uf = colunas[2].get_text(strip=True)
		link_tag = colunas[3].find("a")
		pagina_parlamentar = ""
		if link_tag and link_tag.get("href"):
			pagina_parlamentar = urljoin(url, str(link_tag["href"]))

		codigo_casa = linha.get("data-casa", "")
		casa = _normaliza_casa(codigo_casa)

		parlamentares.append(
			{
				"nome": nome,
				"partido": partido,
				"uf": uf,
				"casa": casa,
				"codigo_casa": codigo_casa,
				"pagina_parlamentar": pagina_parlamentar,
			}
		)

	if not parlamentares:
		raise RuntimeError("Nao foi possivel extrair parlamentares da pagina.")

	return parlamentares


def enriquecer_parlamentares(
	parlamentares: list[dict[str, Any]], timeout: int = 30, atraso: float = 0.0
) -> list[dict[str, Any]]:
	sessao = requests.Session()
	sessao.headers.update(
		{
			"User-Agent": (
				"Mozilla/5.0 (X11; Linux x86_64) "
				"AppleWebKit/537.36 (KHTML, like Gecko) "
				"Chrome/127.0.0.0 Safari/537.36"
			)
		}
	)

	dados_enriquecidos: list[dict[str, Any]] = []
	for parlamentar in parlamentares:
		pagina = str(parlamentar.get("pagina_parlamentar", ""))
		perfil = extrair_dados_pagina_parlamentar(pagina, sessao=sessao, timeout=timeout)
		registro = {**parlamentar, "perfil": perfil, "filtros": perfil.get("filtros", {})}
		dados_enriquecidos.append(registro)

		if atraso > 0:
			time.sleep(atraso)

	return dados_enriquecidos


def gerar_catalogo_campos(dados: list[dict[str, Any]]) -> list[dict[str, Any]]:
	estatisticas: dict[str, dict[str, Any]] = {}
	total = len(dados)

	for registro in dados:
		filtros = registro.get("filtros", {})
		if not isinstance(filtros, dict):
			continue
		for campo, valor in filtros.items():
			if campo not in estatisticas:
				estatisticas[campo] = {
					"campo": campo,
					"preenchidos": 0,
					"percentual_preenchido": 0.0,
					"exemplos": [],
				}

			if valor not in ("", None, [], {}):
				estatisticas[campo]["preenchidos"] += 1
				exemplos = estatisticas[campo]["exemplos"]
				if len(exemplos) < 5 and valor not in exemplos:
					exemplos.append(valor)

	resultado = []
	for campo in sorted(estatisticas.keys()):
		item = estatisticas[campo]
		preenchidos = item["preenchidos"]
		item["percentual_preenchido"] = round((preenchidos / total) * 100, 2) if total else 0.0
		resultado.append(item)

	return resultado


def salvar_json(dados: list[dict[str, Any]], caminho: Path) -> None:
	caminho.parent.mkdir(parents=True, exist_ok=True)
	with caminho.open("w", encoding="utf-8") as arquivo:
		json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def salvar_csv(dados: list[dict[str, Any]], caminho: Path) -> None:
	caminho.parent.mkdir(parents=True, exist_ok=True)
	campos = [
		"nome",
		"partido",
		"uf",
		"casa",
		"codigo_casa",
		"pagina_parlamentar",
		"perfil_titulo",
		"perfil_descricao",
		"perfil_foto",
		"perfil_dominio",
		"perfil_erro",
		"filtros_json",
	]

	linhas = []
	for item in dados:
		perfil = item.get("perfil", {}) if isinstance(item.get("perfil"), dict) else {}
		linha = {
			"nome": item.get("nome", ""),
			"partido": item.get("partido", ""),
			"uf": item.get("uf", ""),
			"casa": item.get("casa", ""),
			"codigo_casa": item.get("codigo_casa", ""),
			"pagina_parlamentar": item.get("pagina_parlamentar", ""),
			"perfil_titulo": perfil.get("titulo", ""),
			"perfil_descricao": perfil.get("descricao", ""),
			"perfil_foto": perfil.get("foto", ""),
			"perfil_dominio": perfil.get("dominio", ""),
			"perfil_erro": perfil.get("erro", ""),
			"filtros_json": json.dumps(item.get("filtros", {}), ensure_ascii=False),
		}
		linhas.append(linha)

	with caminho.open("w", encoding="utf-8", newline="") as arquivo:
		writer = csv.DictWriter(arquivo, fieldnames=campos)
		writer.writeheader()
		writer.writerows(linhas)


def resolver_diretorio_saida(caminho_saida: str) -> Path:
	base = Path(caminho_saida)
	if not base.is_absolute():
		base = Path.cwd() / base

	try:
		base.mkdir(parents=True, exist_ok=True)
		return base
	except PermissionError:
		fallback = Path.cwd() / caminho_saida.lstrip("/")
		fallback.mkdir(parents=True, exist_ok=True)
		print(
			"Aviso: sem permissao para gravar em "
			f"{base}. Usando {fallback} no projeto atual."
		)
		return fallback


def main() -> None:
	parser = argparse.ArgumentParser(
		description=(
			"Extrai e enriquece dados de parlamentares em exercicio do Congresso Nacional."
		)
	)
	parser.add_argument(
		"--url",
		default=URL_PARLAMENTARES,
		help="URL da pagina de parlamentares em exercicio.",
	)
	parser.add_argument("--saida-dir", default=SAIDA_PADRAO, help="Diretorio de saida.")
	parser.add_argument(
		"--max-parlamentares",
		type=int,
		default=0,
		help="Limita a quantidade de parlamentares processados (0 = todos).",
	)
	parser.add_argument(
		"--timeout",
		type=int,
		default=30,
		help="Timeout das requisicoes em segundos.",
	)
	parser.add_argument(
		"--atraso",
		type=float,
		default=0.0,
		help="Atraso (segundos) entre requisicoes dos perfis.",
	)
	args = parser.parse_args()

	diretorio_saida = resolver_diretorio_saida(args.saida_dir)

	parlamentares = extrair_parlamentares_em_exercicio(args.url)
	if args.max_parlamentares > 0:
		parlamentares = parlamentares[: args.max_parlamentares]

	dados = enriquecer_parlamentares(
		parlamentares,
		timeout=args.timeout,
		atraso=args.atraso,
	)

	catalogo_campos = gerar_catalogo_campos(dados)

	arquivo_base_json = diretorio_saida / "parlamentares_base.json"
	arquivo_enriquecido_json = diretorio_saida / "parlamentares_enriquecidos.json"
	arquivo_enriquecido_csv = diretorio_saida / "parlamentares_enriquecidos.csv"
	arquivo_catalogo = diretorio_saida / "catalogo_campos.json"

	salvar_json(parlamentares, arquivo_base_json)
	salvar_json(dados, arquivo_enriquecido_json)
	salvar_csv(dados, arquivo_enriquecido_csv)
	salvar_json(catalogo_campos, arquivo_catalogo)

	print(f"Parlamentares extraidos: {len(dados)}")
	print(f"Base JSON: {arquivo_base_json}")
	print(f"Dados enriquecidos JSON: {arquivo_enriquecido_json}")
	print(f"Dados enriquecidos CSV: {arquivo_enriquecido_csv}")
	print(f"Catalogo de campos JSON: {arquivo_catalogo}")


if __name__ == "__main__":
	main()
