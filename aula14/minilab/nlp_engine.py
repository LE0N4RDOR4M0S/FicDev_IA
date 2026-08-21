"""NLP engine for OCR cleanup and linguistic analysis."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

import spacy

_nlp = None


def _carregar_modelo() -> spacy.Language:
    """Load the spaCy model once and reuse it."""
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("pt_core_news_sm")
        except OSError as exc:
            raise OSError(
                "Modelo spaCy nao encontrado. Execute: python -m spacy download pt_core_news_sm"
            ) from exc
    return _nlp


def limpar_ocr(texto: str) -> str:
    """Remove typical OCR artifacts and normalize whitespace."""
    texto = re.sub(r"-(\n)(\w)", r"\2", texto)
    texto = re.sub(r"(?<!\n)\n(?!\n)", " ", texto)
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", texto)
    texto = re.sub(r"\.{3,}", "...", texto)
    texto = re.sub(r",{2,}", ",", texto)

    linhas = texto.split("\n")
    linhas = [
        linha
        for linha in linhas
        if len(re.findall(r"[a-záéíóúàâêôãõüç]", linha, re.I)) >= 3 or linha.strip() == ""
    ]
    return "\n".join(linhas).strip()


def tokenizar(texto: str, tamanho_min: int = 3) -> list[str]:
    """Tokenize, remove stopwords and lemmatize the text."""
    nlp = _carregar_modelo()
    doc = nlp(texto.lower())
    return [
        token.lemma_
        for token in doc
        if token.is_alpha and not token.is_stop and not token.is_punct and len(token.text) >= tamanho_min
    ]


def extrair_entidades(texto: str) -> dict[str, list[str]]:
    """Recognize named entities and group them by label."""
    nlp = _carregar_modelo()
    doc = nlp(texto)
    entidades: dict[str, list[str]] = {}

    for entidade in doc.ents:
        entidades.setdefault(entidade.label_, [])
        if entidade.text not in entidades[entidade.label_]:
            entidades[entidade.label_].append(entidade.text)

    return entidades


def analisar(texto_bruto: str, top_n: int = 20) -> dict[str, Any]:
    """Full NLP pipeline: cleanup, tokenization, entity recognition and frequencies."""
    texto_limpo = limpar_ocr(texto_bruto)
    tokens = tokenizar(texto_limpo)
    frequencia = Counter(tokens)
    entidades = extrair_entidades(texto_limpo)

    return {
        "texto_limpo": texto_limpo,
        "total_tokens": len(tokens),
        "vocabulario_unico": len(set(tokens)),
        "top_termos": frequencia.most_common(top_n),
        "entidades": entidades,
        "total_caracteres": len(texto_limpo),
        "total_palavras": len(texto_limpo.split()),
    }