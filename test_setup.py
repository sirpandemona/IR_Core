from pprint import pprint
import SVM


def retrieve_queries() -> list:
    results = []
    file = open("topics.701-850.txt")
    for line in file:
        if line.startswith("<title>"):
            results.append(line.replace("<title>", "").replace("\n", ""))
    return results


queries = retrieve_queries()
dataset = SVM.generateTrainingSet(queries)

pprint(dataset)

