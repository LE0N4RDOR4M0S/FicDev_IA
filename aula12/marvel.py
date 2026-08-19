import requests
import json

marvel_api_url_base = 'https://akabab.github.io/superhero-api/api'

id = -1
requests_params = {
}
try:
    resp = requests.get(f'{marvel_api_url_base}/id/{id}.json', params=requests_params)
    print(resp.status_code)
    print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
except requests.exceptions.HTTPError as e:
    print('Erro na API: ', e, resp.status_code)
except requests.exceptions.Timeout as e:
    print('API demorou demais para responder: ', e)