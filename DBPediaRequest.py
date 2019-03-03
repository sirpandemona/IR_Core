import requests

class DBPediaRequest:
    def __init__(self, subject):
        self.subject = subject

    def get_dbpedia_url(self):
        subjectUnderscore = self.subject.replace(' ', '_')
        return 'http://dbpedia.org/data/' + subjectUnderscore + '.json'

    def get_resource_url(self):
        data = requests.get(self.get_dbpedia_url()).json()
        return data['http://dbpedia.org/resource/' + self.subject.replace(' ', '_')]

    def get_related_subject_list(self):
        resource = self.get_resource_url()
        result_list = []
        for key in sorted(resource):
            key_split = key.split('/')
            result_list.append(key_split[len(key_split)-1])

        return result_list

    def get_all_information_on_subject(self):
        resource = self.get_resource_url()
        information_list = self.get_related_subject_list()

        for key in information_list:
            try:
                print(key + ' ' + str(resource['http://dbpedia.org/ontology/' + key]))
            except KeyError:
                None
            except:
                None
