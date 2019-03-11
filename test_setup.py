from pprint import pprint
import SVM
import pyspotlight


def retrieve_queries() -> list:
    results = []
    file = open("topics.701-850.txt")
    num = 701
    for line in file:
        if line.startswith("<title>"):
            q = line.replace("<title>", "").replace("\n", "")
            results.append((q, num))
            num = num + 1
    return results


def retrieve_concepts(queries: list) -> list:
    results = []
    for q in queries:
        (query, num) = q
        concept_list = pyspotlight.get_relevant_concepts_from_dbpedia(query)
        results.append((query, num, concept_list))
    return results


def retrieve_features(concept_lists: list) -> list:
    results = []
    for cl in concept_lists:
        (query, num, candidate) = cl
        features = SVM.SVM.concepts2feat(candidate, query)
        results.append((num, features))
    return results


qs = retrieve_queries()
# pprint(qs)
cls = retrieve_concepts(qs)
pprint(cls)
fts = retrieve_features(cls)
pprint(fts)
