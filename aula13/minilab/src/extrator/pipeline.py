from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import pdfplumber
from pypdf import PdfReader


def limpar_texto(texto: str) -> str:
    if not texto or not texto.strip():
        return ""

    texto = unicodedata.normalize("NFC", texto)
    texto = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", texto)
    texto = re.sub(r"(\w+)-\n(\w+)", r"\1\2", texto)
    texto = re.sub(r"(?<!\n)\n(?!\n)", " ", texto)
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r" +([.,;:!?])", r"\1", texto)
    return texto.strip()


def preprocessar_para_embedding(texto: str) -> str:
    texto = limpar_texto(texto)
    texto = re.sub(r"https?://\S+|www\.\S+", "[URL]", texto)
    texto = re.sub(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "[EMAIL]", texto)
    texto = re.sub(r"\b\d{6,}\b", "[NUM]", texto)
    return re.sub(r"[ \t]+", " ", texto).strip()


def estimar_tokens(texto: str) -> int:
    return max(1, int(len(texto) / 4))


def chunks_por_tamanho(
    texto: str,
    tamanho_max: int = 1000,
    overlap: int = 200,
    origem: str = "",
) -> list[dict[str, Any]]:
    texto = limpar_texto(texto)
    if not texto:
        return []

    chunks: list[dict[str, Any]] = []
    inicio = 0
    idx = 0

    while inicio < len(texto):
        fim = min(len(texto), inicio + tamanho_max)
        trecho = texto[inicio:fim].strip()

        if not trecho:
            break

        if fim < len(texto):
            ult = trecho.rfind(" ")
            if ult > int(tamanho_max * 0.6):
                trecho = trecho[:ult].rstrip()
                fim = inicio + len(trecho)

        trecho = trecho.strip()
        if trecho:
            chunks.append(
                {
                    "chunk_id": f"{origem}_c{idx:03d}" if origem else f"c{idx:03d}",
                    "texto": trecho,
                    "texto_embed": preprocessar_para_embedding(trecho),
                    "n_chars": len(trecho),
                    "n_tokens_est": estimar_tokens(trecho),
                    "inicio_char": inicio,
                }
            )
            idx += 1

        if fim >= len(texto):
            break

        inicio = max(0, fim - overlap)

    return chunks


def chunks_por_secao(texto: str, max_chars: int = 1000, overlap: int = 200) -> list[dict[str, Any]]:
    texto = limpar_texto(texto)
    if not texto:
        return []

    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    blocos: list[tuple[str, list[str]]] = []
    titulo_atual = "SECAO"
    bloco_atual: list[str] = []

    def eh_titulo(linha: str) -> bool:
        if len(linha) > 80:
            return False
        if not linha:
            return False
        if linha.isupper() and len(linha.split()) <= 10:
            return True
        return bool(re.fullmatch(r"(?:\d+\.?\s*)?(?:[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ0-9\s/&:-]+)", linha))

    for linha in linhas:
        if eh_titulo(linha):
            if bloco_atual:
                blocos.append((titulo_atual, bloco_atual[:]))
            titulo_atual = linha
            bloco_atual = []
            continue
        bloco_atual.append(linha)

    if bloco_atual:
        blocos.append((titulo_atual, bloco_atual[:]))

    sections: list[str] = []
    for titulo, linhas_bloco in blocos:
        conteudo = " ".join(linhas_bloco)
        if conteudo:
            sections.append(f"{titulo}\n{conteudo}")

    if not sections:
        sections = [texto]

    chunks: list[dict[str, Any]] = []
    cursor = 0
    idx = 0
    for secao in sections:
        texto_secao = limpar_texto(secao)
        if not texto_secao:
            continue
        for chunk in chunks_por_tamanho(texto_secao, tamanho_max=max_chars, overlap=overlap, origem=f"secao_{idx:03d}"):
            chunk["titulo_secao"] = secao.splitlines()[0][:120]
            chunks.append(chunk)
        idx += 1

    return chunks


def extrair_tabelas_pagina(pagina: Any) -> list[dict[str, Any]]:
    tabelas = pagina.extract_tables() or []
    saida: list[dict[str, Any]] = []

    for idx, tabela in enumerate(tabelas):
        if not tabela or not tabela[0]:
            continue
        headers = tabela[0]
        rows = tabela[1:]
        df = pd.DataFrame(rows, columns=headers)
        saida.append(
            {
                "tabela_id": f"t{idx:02d}",
                "colunas": list(df.columns),
                "linhas": df.to_dict(orient="records"),
            }
        )

    return saida


def extrair_pdf(
    caminho: str | Path,
    tamanho_chunk: int = 1000,
    overlap: int = 200,
    metodo_chunk: str = "tamanho",
) -> dict[str, Any]:
    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    reader = PdfReader(str(caminho))
    metadata = reader.metadata or {}
    n_pags = len(reader.pages)

    doc_meta = {
        "arquivo": caminho.name,
        "n_paginas": n_pags,
        "titulo": getattr(metadata, "title", None) or caminho.stem,
        "autor": getattr(metadata, "author", None) or "Desconhecido",
        "produtor": getattr(metadata, "producer", None) or "",
        "extraido_em": datetime.now().isoformat(timespec="seconds"),
        "biblioteca": "pdfplumber",
        "metodo_chunk": metodo_chunk,
        "chunk_size": tamanho_chunk,
        "chunk_overlap": overlap,
        "aviso_escaneado": False,
    }

    paginas: list[dict[str, Any]] = []
    chunks_total: list[dict[str, Any]] = []
    origem = caminho.stem

    with pdfplumber.open(str(caminho)) as pdf:
        for i, pag in enumerate(pdf.pages):
            num_pag = i + 1
            texto_bruto = pag.extract_text() or ""
            texto_limpo = limpar_texto(texto_bruto)
            tabelas = extrair_tabelas_pagina(pag)

            paginas.append(
                {
                    "pagina": num_pag,
                    "texto": texto_limpo,
                    "n_chars": len(texto_limpo),
                    "n_tokens_est": estimar_tokens(texto_limpo),
                    "vazia": len(texto_limpo.strip()) == 0,
                    "tabelas": tabelas,
                }
            )

            if not texto_limpo.strip():
                continue

            if metodo_chunk == "secao":
                chunks_pag = chunks_por_secao(texto_limpo, max_chars=tamanho_chunk, overlap=overlap)
            else:
                chunks_pag = chunks_por_tamanho(
                    texto_limpo,
                    tamanho_max=tamanho_chunk,
                    overlap=overlap,
                    origem=f"{origem}_p{num_pag:03d}",
                )

            for chunk in chunks_pag:
                chunk["pagina"] = num_pag
                chunks_total.append(chunk)

    if paginas:
        textos = [p["n_chars"] for p in paginas if not p["vazia"]]
        if textos and (sum(textos) / len(textos)) < 100:
            doc_meta["aviso_escaneado"] = True
            print("PDF possivelmente escaneado — considere OCR (Aula 14)")

    return {
        "documento": doc_meta,
        "paginas": paginas,
        "chunks": chunks_total,
    }


def imprimir_resumo(resultado: dict[str, Any]) -> None:
    doc = resultado["documento"]
    pags = resultado["paginas"]
    chunks = resultado["chunks"]

    sep = "=" * 55
    print(f"\n{sep}")
    print(" EXTRAÇÃO DE PDF")
    print(sep)
    print(f" Arquivo : {doc['arquivo']}")
    print(f" Título : {doc['titulo']}")
    print(f" Autor : {doc['autor']}")
    print(f" Páginas : {doc['n_paginas']}")
    print(f" Extraído : {doc['extraido_em']}")

    vazias = sum(1 for p in pags if p["vazia"])
    total_chars = sum(p["n_chars"] for p in pags)
    total_tokens = sum(p["n_tokens_est"] for p in pags)
    print(f"\n Páginas com texto : {doc['n_paginas'] - vazias}")
    print(f" Páginas vazias : {vazias}")
    print(f" Total de chars : {total_chars:,}")
    print(f" Tokens estimados : {total_tokens:,}")

    print(f"\n Chunks gerados : {len(chunks)}")
    if chunks:
        tamanhos = [c["n_chars"] for c in chunks]
        media = sum(tamanhos) / len(tamanhos)
        print(f" Chunk mín/méd/máx : {min(tamanhos)} / {media:.1f} / {max(tamanhos)} chars")
        tokens = [c["n_tokens_est"] for c in chunks]
        media_tokens = sum(tokens) / len(tokens)
        print(f" Tokens mín/méd/máx: {min(tokens)} / {media_tokens:.1f} / {max(tokens)}")

    print(f"\n Prévia (primeiros 3 chunks):")
    for c in chunks[:3]:
        preview = c["texto"][:120].replace("\n", " ")
        print(f" [{c['chunk_id']}] ({c['n_chars']} chars, p.{c['pagina']})")
        print(f" {preview}...")

    print(f"\n{sep}\n")


def salvar_json(dados: dict[str, Any], caminho: str | Path) -> None:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f" Salvo: {caminho}")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv if argv is None else argv

    if len(argv) < 2:
        print("Uso: python extrator_pdf.py <arquivo.pdf> [chunk_size] [overlap] [--metodo tamanho|secao]")
        print("Ex: python extrator_pdf.py documento.pdf 1000 200")
        return 1

    caminho = Path(argv[1])
    chunk_size = int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else 1000
    overlap = int(argv[3]) if len(argv) > 3 and argv[3].isdigit() else 200
    metodo_chunk = "tamanho"
    if len(argv) > 4:
        metodo_chunk = argv[4].replace("--metodo=", "")

    print(f"Processando: {caminho.name} ...")
    resultado = extrair_pdf(caminho, chunk_size, overlap, metodo_chunk)
    imprimir_resumo(resultado)

    saida_paginas = Path("paginas.json")
    saida_chunks = Path("chunks.json")
    salvar_json({"documento": resultado["documento"], "paginas": resultado["paginas"]}, saida_paginas)
    salvar_json({"documento": resultado["documento"], "chunks": resultado["chunks"]}, saida_chunks)

    nome_base = caminho.stem
    salvar_json({"documento": resultado["documento"], "paginas": resultado["paginas"]}, Path(f"{nome_base}_paginas.json"))
    salvar_json({"documento": resultado["documento"], "chunks": resultado["chunks"]}, Path(f"{nome_base}_chunks.json"))

    print(f"Concluído! {len(resultado['chunks'])} chunks exportados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
