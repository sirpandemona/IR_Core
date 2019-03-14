import requests
import rdflib
from pprint import pprint

class DBPediaRequest:
    def __init__(self, uri):
        self.dbpedia_url = 'http://dbpedia.org/data/' + uri + '.json'
        self.uri = uri
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

    def get_uri(self):
        return self.uri

    def get_abstract_of_subject(self) -> str:
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

        # If the abstract is not found in the .json file, do an extra check on the rdf file to find the abstract
        try:
            return self.get_abstract_from_rdf()
        except IndexError:
            # No abstract found in rdf file for this subject
            pass

    def get_abstract_from_rdf(self) -> str:
        g = rdflib.Graph()
        g.load('http://dbpedia.org/resource/' + self.uri)
        semweb = rdflib.URIRef('http://dbpedia.org/resource/' + self.uri)
        dbpedia = rdflib.Namespace('http://dbpedia.org/ontology/')

        return list(x for x in g.objects(semweb, dbpedia['abstract']) if x.language == 'en')[0]
