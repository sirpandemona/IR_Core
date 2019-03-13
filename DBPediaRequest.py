import requests
from pprint import pprint

class DBPediaRequest:
    def __init__(self, uri):
        self.dbpedia_url = 'http://dbpedia.org/data/' + uri + '.json'

        data = requests.get(self.dbpedia_url).json()
        self.resource = data['http://dbpedia.org/resource/' + uri]

    def get_related_subject_list(self) -> list:
        result_list = []

        for key in sorted(self.resource):
            key_split = key.split('/')
            result_list.append(key_split[len(key_split)-1])

        return result_list

    def get_dbpedia_url(self):
        return str(self.dbpedia_url)

    def get_abstract_of_subject(self):
        information_list = self.get_related_subject_list()
        key = information_list[0]
        abstracts = self.resource['http://dbpedia.org/ontology/' + key]

        for entry in abstracts:
            try:
                if entry['lang'] == 'en':
                    return entry['value']
                else:
                    continue
            except KeyError:
                # Last entry of abstracts has no index called 'lang', do nothing but catch error
                pass

