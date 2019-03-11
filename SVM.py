from pprint import pprint

from sklearn import svm, preprocessing
import numpy as np
from pyspotlight import get_relevant_concepts_from_dbpedia


# dummy data
# train_x = [[1], [2], [3], [4]]
# train_y = [ 0, 0, 1,2]
# test_x = [[0], [2.3], [5]]

# training the svm
# scaler = preprocessing.StandardScaler().fit(train_x)
# train_x_norm = scaler.transform(train_x)
# clf = svm.SVC(gamma='scale', decision_function_shape='ovo',kernel='poly')
# clf.fit(train_x_norm ,train_y)

# using the svm for classifying unknown objects
# test_x_norm = scaler.transform(test_x)
# unkw_y = clf.predict(test_x_norm)
# print(unkw_y)

def concepts2feat(concept_list: list, query: str) -> np.ndarray:
    rank = 0
    n_rel_art = concept_list.__len__()
    n_feats = 5
    results = []
    for candidates in concept_list:
        res = candidates['resource']
        if isinstance(res, dict):
            res = [res]
        n_res = res.__len__()
        feature_vector = np.zeros((n_res, n_feats))
        count = 0
        for resource in res:
            feature_vector[count, 0] = resource['contextualScore']
            feature_vector[count, 1] = resource['finalScore']
            feature_vector[count, 2] = resource['support']
            feature_vector[count, 3] = rank
            teq = resource['label'] == query  # title equals query
            if teq:
                feature_vector[count, 4] = 1
            count = count+1
        rank = rank + 1
        if results.__len__() == 0:
            results = feature_vector
        else:
            results = np.append(results, feature_vector, axis=0)
    return results


def generateTrainingSet(queries: list) -> np.ndarray:
    training_data = []
    for query in queries:
        cl = get_relevant_concepts_from_dbpedia(query)
        if cl:
            feats = concepts2feat(cl, query)
            if training_data.__len__() == 0:
                training_data = feats
            else:
                training_data = np.append(training_data, feats, axis=0)
    training_data = np.array(training_data)
    return training_data


# query = "obama white house audience"
# cl = get_relevant_concepts_from_dbpedia(query)
qs = ["barrack obama speech white house", "donald trump speech white house"]
train_data = generateTrainingSet(qs)
training_labels = [1, 1, 0, 0]
scaler = preprocessing.StandardScaler().fit(train_data)
train_x_norm = scaler.transform(train_data)
clf = svm.SVC(gamma='scale', decision_function_shape='ovo', kernel='poly')
clf.fit(train_x_norm, training_labels)
