import requests


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
        return self.dbpedia_url

    def print_all_information_of_subject(self):
        information_list = self.get_related_subject_list()
        print(self.dbpedia_url)
        for key in information_list:
            try:
                print(key + ': ' + str(self.resource['http://dbpedia.org/ontology/' + key]))
            except KeyError:
                pass
