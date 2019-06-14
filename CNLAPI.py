import requests

print('Running')
URI = 'https://language.googleapis.com/$discovery/rest?version=v1'
ANALYZE_SENTIMENT = f"{URI}"
resp = requests.get(URI)
if resp.status_code != 200:
	raise ApiError(f'GET /URI/ {resp.status_code}')
print(dir(resp))

for x, y in resp.json().items():
	print(f"{x}: {y}", end="\n\n")

