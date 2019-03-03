import requests
import sys


class DBPediaRequest:
    def __init__(self, subject):
        subject_underscore = subject.replace(' ', '_')
        self.dbpedia_url = 'http://dbpedia.org/data/' + subject_underscore + '.json'

        data = requests.get(self.dbpedia_url).json()
        try:
            self.resource = data['http://dbpedia.org/resource/' + subject.replace(' ', '_')]
        except KeyError:
            print('This dbpedia entry does not exist')
            sys.exit()

        # If a common misspelling of a query is encountered, go to the redirected (and thus correct) page
        if len(self.get_related_subject_list()) is 7:
            new_resource = self.resource['http://dbpedia.org/ontology/wikiPageRedirects'][0]['value']
            new_resource_split = new_resource.split('/')
            new_subject = new_resource_split[len(new_resource_split) - 1]

            self.dbpedia_url = 'http://dbpedia.org/data/' + new_subject + '.json'
            data = requests.get(self.dbpedia_url).json()

            try:
                self.resource = data['http://dbpedia.org/resource/' + new_subject]
            except KeyError:
                print('This dbpedia entry does not exist')
                sys.exit()

    def get_related_subject_list(self):
        result_list = []
        for key in sorted(self.resource):
            key_split = key.split('/')
            result_list.append(key_split[len(key_split)-1])

        return result_list

    def get_all_information_on_subject(self):
        information_list = self.get_related_subject_list()

        for key in information_list:
            try:
                print(key + ' ' + str(self.resource['http://dbpedia.org/ontology/' + key]))
            except KeyError:
                None
            except:
                None