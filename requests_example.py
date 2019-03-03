import requests

data = requests.get('http://dbpedia.org/data/Matteo_Donati.json').json()
matteo = data['http://dbpedia.org/resource/Matteo_Donati']

for key in sorted(matteo): print(key)