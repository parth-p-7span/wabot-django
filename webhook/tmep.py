import requests

url = "https://gist.githubusercontent.com/parthp-7span/03fed9ab3a1c028db6fb69dafde36e49/raw/4f79a4a7f5d9c6d02147f8ee78c48192fb788fca/actions.json"

res = requests.get(url)

print(type(res.json()))
