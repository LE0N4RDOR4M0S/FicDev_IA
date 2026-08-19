"""
Consulta endereços brasileiros a partir de CEPs usando a API ViaCEP.

Suporta múltiplas consultas em sequência e trata todos os erros
comuns: CEP inválido, não encontrado, timeout e erro de rede.
"""

from __future__ import annotations

import re

import requests

# ── Constantes ──────────────────────────────────────────────

BASE_URL = "https://viacep.com.br/ws/{cep}/json/"
TIMEOUT = 8


# ── Funções ─────────────────────────────────────────────────

def limpar_cep(cep_raw: str) -> str:
    """Remove traços, pontos e espaços do CEP, retornando apenas dígitos."""
    return re.sub(r"\D", "", cep_raw)


def validar_cep(cep: str) -> bool:
    """Verifica se o CEP tem exatamente 8 dígitos numéricos."""
    return len(cep) == 8 and cep.isdigit()


def consultar_cep(cep: str) -> dict | None:
    """Consulta a API ViaCEP e retorna os dados do endereço."""
    url = BASE_URL.format(cep=cep)

    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()

        dados = resp.json()

        if dados.get("erro"):
            return None

        return dados

    except requests.exceptions.HTTPError as e:
        print(f"  Erro HTTP {e.response.status_code}: {e}")
    except requests.exceptions.ConnectionError:
        print("  Erro de conexão: verifique sua internet.")
    except requests.exceptions.Timeout:
        print(f"  Timeout: servidor demorou mais de {TIMEOUT}s.")
    except requests.exceptions.RequestException as e:
        print(f"  Erro inesperado: {e}")

    return None


def exibir_endereco(dados: dict) -> None:
    """Exibe os dados do endereço de forma formatada no terminal."""
    cep_fmt = f"{dados['cep']}"

    linhas = [
        ("CEP", cep_fmt),
        ("Logradouro", dados.get("logradouro", "—")),
        ("Complemento", dados.get("complemento") or "—"),
        ("Bairro", dados.get("bairro", "—")),
        ("Cidade", dados.get("localidade", "—")),
        ("Estado", f"{dados.get('uf', '—')} ({dados.get('estado', '—')})"),
        ("IBGE", dados.get("ibge", "—")),
        ("DDD", dados.get("ddd", "—")),
    ]

    print()
    print("  " + "=" * 44)
    for campo, valor in linhas:
        print(f"  {campo:<14}: {valor}")
    print("  " + "=" * 44)


def main() -> None:
    """Loop principal: aceita múltiplas consultas até o usuário sair."""
    print("=" * 48)
    print("        CONSULTOR DE CEP — ViaCEP")
    print("  Digite um CEP para buscar o endereço.")
    print("  Formatos aceitos: 01310-100  ou  01310100")
    print("  Digite 'sair' para encerrar.")
    print("=" * 48)

    while True:
        entrada = input("\nCEP: ").strip()

        if entrada.lower() in ("sair", "exit", "q"):
            print("Encerrando. Até logo!")
            break

        cep = limpar_cep(entrada)

        if not validar_cep(cep):
            print(f"  CEP inválido: \"{entrada}\" — informe 8 dígitos numéricos.")
            continue

        print(f"  Consultando CEP {cep[:5]}-{cep[5:]}...", end="", flush=True)

        dados = consultar_cep(cep)

        if dados:
            exibir_endereco(dados)
        else:
            print()
            print(f"  CEP {cep[:5]}-{cep[5:]} não encontrado na base dos Correios.")


if __name__ == "__main__":
    main()
