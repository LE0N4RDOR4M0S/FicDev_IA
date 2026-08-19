import requests

cep_inexistente = "00000000"
url = f"https://viacep.com.br/ws/{cep_inexistente}/json/"

try:
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    dados = resp.json()
    
    if dados.get("erro"):
        print("Erro de negócio: CEP não encontrado na base dos Correios.")
    else:
        print("Endereço encontrado:", dados.get("logradouro"))

except requests.exceptions.HTTPError as e:
    print(f"Erro HTTP {e.response.status_code}: A requisição falhou no servidor.")
except requests.exceptions.ConnectionError as e:
    print("Erro de Rede: Verifique sua conexão ou a URL inserida.", e.response.status_code)
except requests.exceptions.Timeout:
    print("Timeout: A requisição demorou mais de 5 segundos.")

cep_valido = "78048906"
try:
    resp_valida = requests.get(f"https://viacep.com.br/ws/{cep_valido}/json/", timeout=(3, 10))
    if resp_valida.status_code == 200:
        dados_sp = resp_valida.json()
        print("\n--- Consulta realizada com sucesso ---")
        print(f"Logradouro: {dados_sp['logradouro']}")
        print(f"Bairro: {dados_sp['bairro']}")
        print(f"Cidade/UF: {dados_sp['localidade']}/{dados_sp['uf']}")
except requests.exceptions.HTTPError as e:
    print(f"Erro HTTP {e.response.status_code}: A requisição falhou no servidor.")
except requests.exceptions.ConnectionError as e:
    print("Erro de Rede: Verifique sua conexão ou a URL inserida.", e.response.status_code)
except requests.exceptions.Timeout:
    print("Timeout: A requisição demorou mais de 5 segundos.")
