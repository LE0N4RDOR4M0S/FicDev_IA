import requests
import json

# resp = requests.get('https://viacep.com.br/ws/78048906/json/')

# print(json.dumps(resp.json(), indent=4, ensure_ascii=False))

## Requisição com parâmetros
url = 'https://api.github.com/search/repositories'

params = {
    'q': 'rootL_CDC_Publisher',
    'language': 'python',
    'page': 1,
    'per_page': 1
}
resp_github = requests.get(url, params=params)
print(resp_github.url)
print(resp_github.status_code)
print(json.dumps(resp_github.json(), indent=4, ensure_ascii=False))

