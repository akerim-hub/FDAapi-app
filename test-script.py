import requests

BASE_URL = "https://api.fda.gov/animalandveterinary/event.json"

limit =1000
skip = True
timeout = 10
params = {"limit": limit}
resp = requests.get(BASE_URL, params=params, timeout=timeout)
resp.raise_for_status()  # raises for 4xx/5xx
print(resp.json())