"""Orchestrates OCR, NLP and result saving."""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

import nlp_engine
import ocr_engine


def processar_documento(caminho_entrada: str, dir_saida: str = ".", top_n: int = 20) -> dict[str, Any]:
    """Run the full pipeline over a scanned document."""
    os.makedirs(dir_saida, exist_ok=True)

    nome_base = os.path.splitext(os.path.basename(caminho_entrada))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefixo = f"{nome_base}_{timestamp}"

    print(f"[1/3] OCR: {caminho_entrada}")
    resultado_ocr = ocr_engine.extrair_texto(caminho_entrada)
    texto_bruto = resultado_ocr["texto"]
    print(f"      Extraidos: {resultado_ocr['caracteres']} caracteres")

    print("[2/3] NLP: limpeza e analise linguistica")
    resultado_nlp = nlp_engine.analisar(texto_bruto, top_n=top_n)
    print(
        f"      Tokens: {resultado_nlp['total_tokens']} | Vocabulario unico: {resultado_nlp['vocabulario_unico']}"
    )

    print("[3/3] Salvando resultados...")
    arq_bruto = os.path.join(dir_saida, f"{prefixo}_bruto.txt")
    with open(arq_bruto, "w", encoding="utf-8") as arquivo_bruto:
        arquivo_bruto.write(texto_bruto)

    arq_limpo = os.path.join(dir_saida, f"{prefixo}_limpo.txt")
    with open(arq_limpo, "w", encoding="utf-8") as arquivo_limpo:
        arquivo_limpo.write(resultado_nlp["texto_limpo"])

    metadados = {
        "arquivo_origem": caminho_entrada,
        "processado_em": datetime.now().isoformat(),
        "ocr": {
            "caracteres_brutos": resultado_ocr["caracteres"],
            "modo_usado": resultado_ocr.get("modo_usado", "n/a"),
        },
        "nlp": {
            "total_palavras": resultado_nlp["total_palavras"],
            "total_tokens": resultado_nlp["total_tokens"],
            "vocabulario_unico": resultado_nlp["vocabulario_unico"],
            "top_termos": resultado_nlp["top_termos"],
            "entidades": resultado_nlp["entidades"],
        },
        "saidas": {
            "texto_bruto": arq_bruto,
            "texto_limpo": arq_limpo,
        },
    }

    arq_json = os.path.join(dir_saida, f"{prefixo}_metadados.json")
    with open(arq_json, "w", encoding="utf-8") as arquivo_json:
        json.dump(metadados, arquivo_json, ensure_ascii=False, indent=2)

    print(f"      Texto bruto : {arq_bruto}")
    print(f"      Texto limpo : {arq_limpo}")
    print(f"      Metadados   : {arq_json}")

    return {**resultado_ocr, **resultado_nlp, "metadados": metadados}


def exibir_resumo(resultado: dict[str, Any]) -> None:
    """Print a human-friendly summary of the pipeline result."""
    print()
    print("=" * 56)
    print("  RESUMO DO PROCESSAMENTO")
    print("=" * 56)
    print(f"  Arquivo       : {resultado['arquivo']}")
    print(f"  Caracteres    : {resultado['caracteres']}")
    print(f"  Palavras      : {resultado['total_palavras']}")
    print(f"  Tokens unicos : {resultado['vocabulario_unico']}")
    print()
    print("  Top 10 termos mais frequentes:")

    for indice, (termo, freq) in enumerate(resultado["top_termos"][:10], 1):
        print(f"    {indice:2}. {termo:<20} {freq}x")

    if resultado["entidades"]:
        print()
        print("  Entidades reconhecidas:")
        for tipo, lista in sorted(resultado["entidades"].items()):
            print(f"    {tipo:<8}: {', '.join(lista[:5])}")

    print("=" * 56)