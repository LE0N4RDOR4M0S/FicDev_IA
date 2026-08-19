import requests
import json

url_base = 'https://pokeapi.co/api/v2/'

params = {
    'limit': 10,
    'offset': 0
}
resp = requests.get(f'{url_base}/pokemon', params=params)
print(resp.status_code)
print(json.dumps(resp.json(), indent=4, ensure_ascii=False))