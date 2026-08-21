"""OCR engine for scanned images and PDFs."""

from __future__ import annotations

import os
from typing import Any

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

try:
    from pdf2image import convert_from_path

    PDF_SUPORTADO = True
except ImportError:
    PDF_SUPORTADO = False


CONFIG_TESS = "--oem 3 --psm 6 -l por"
DPI_PADRAO = 300


def _prep_pillow(img: Image.Image) -> Image.Image:
    """Light preprocessing with Pillow for cleaner images."""
    img = img.convert("L")
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    img = img.filter(ImageFilter.SHARPEN)

    width, height = img.size
    if width < 2000:
        scale = 2000 / width
        img = img.resize((int(width * scale), int(height * scale)), Image.LANCZOS)

    return img


def _prep_opencv(img: Image.Image) -> Image.Image:
    """Robust preprocessing with OpenCV for difficult images."""
    arr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    arr = cv2.fastNlMeansDenoising(arr, h=10)
    arr = cv2.adaptiveThreshold(
        arr,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10,
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    arr = cv2.morphologyEx(arr, cv2.MORPH_OPEN, kernel)
    return Image.fromarray(arr)


def ocr_imagem(caminho: str, modo: str = "auto") -> dict[str, Any]:
    """Extract text from a PNG, JPEG, TIFF or similar image."""
    img_original = Image.open(caminho).convert("RGB")
    texto = ""
    modo_usado = "pillow"

    if modo in ("pillow", "auto"):
        img_proc = _prep_pillow(img_original)
        texto = pytesseract.image_to_string(img_proc, config=CONFIG_TESS)
        modo_usado = "pillow"

    if modo == "auto" and len(texto.strip()) < 200:
        img_proc = _prep_opencv(img_original)
        texto = pytesseract.image_to_string(img_proc, config=CONFIG_TESS)
        modo_usado = "opencv (fallback)"

    if modo == "opencv":
        img_proc = _prep_opencv(img_original)
        texto = pytesseract.image_to_string(img_proc, config=CONFIG_TESS)
        modo_usado = "opencv"

    return {
        "arquivo": os.path.basename(caminho),
        "modo_usado": modo_usado,
        "texto": texto.strip(),
        "caracteres": len(texto.strip()),
    }


def ocr_pdf(caminho: str, dpi: int = DPI_PADRAO) -> dict[str, Any]:
    """Extract text from all pages of a scanned PDF."""
    if not PDF_SUPORTADO:
        raise ImportError("pdf2image nao instalado. Execute: pip install pdf2image")

    print(f"Convertendo PDF ({dpi} DPI)...")
    imagens = convert_from_path(caminho, dpi=dpi, fmt="png", thread_count=4)

    paginas = []
    for indice, imagem in enumerate(imagens, 1):
        print(f"  OCR pagina {indice}/{len(imagens)}...", end=" ", flush=True)
        imagem_proc = _prep_pillow(imagem)
        texto = pytesseract.image_to_string(imagem_proc, config=CONFIG_TESS).strip()
        paginas.append({"pagina": indice, "texto": texto, "caracteres": len(texto)})
        print(f"{len(texto)} chars")

    texto_completo = "\n\n".join(pagina["texto"] for pagina in paginas)
    return {
        "arquivo": os.path.basename(caminho),
        "total_paginas": len(paginas),
        "paginas": paginas,
        "texto_completo": texto_completo,
        "texto": texto_completo,
        "caracteres": len(texto_completo),
    }


def extrair_texto(caminho: str, **kwargs: Any) -> dict[str, Any]:
    """Detect the file type and call the appropriate OCR routine."""
    extensao = os.path.splitext(caminho)[1].lower()
    if extensao == ".pdf":
        return ocr_pdf(caminho, **kwargs)
    return ocr_imagem(caminho, **kwargs)