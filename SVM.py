from pprint import pprint

from sklearn import svm, preprocessing
import numpy as np
from pyspotlight import get_relevant_concepts_from_dbpedia
#dummy data
#train_x = [[1], [2], [3], [4]]
#train_y = [ 0, 0, 1,2]
#test_x = [[0], [2.3], [5]]

#training the svm
#scaler = preprocessing.StandardScaler().fit(train_x)
#train_x_norm = scaler.transform(train_x)
#clf = svm.SVC(gamma='scale', decision_function_shape='ovo',kernel='poly')
#clf.fit(train_x_norm ,train_y)

#using the svm for classifying unknown objects
#test_x_norm = scaler.transform(test_x)
#unkw_y = clf.predict(test_x_norm)
#print(unkw_y)

def concepts2feat( concept_list : list, query:str ) -> np.ndarray:
    rank = 0
    n_rel_art = concept_list.__len__()
    n_feats = 5
    results = np.zeros((n_rel_art, n_feats))
    for candidate in concept_list:
        results[rank, 0] = candidate['resource']['contextualScore']
        results[rank, 1] = candidate['resource']['finalScore']
        results[rank, 2] = candidate['resource']['support']
        results[rank,3] = rank
        teq = candidate['resource']['label'] == query #title equals query
        if teq:
            results[rank, 4] = 1
        rank = rank+1
    return results

def generateTrainingSet(queries : list) -> np.ndarray:
    training_data = []
    for query in queries:
        cl = get_relevant_concepts_from_dbpedia(query)
        feats = concepts2feat(cl, query)
        if training_data == []:
            training_data = feats
        else:
            training_data = np.append(training_data, feats, axis=0)
    training_data = np.array(training_data)
    return training_data


#query = "obama white house audience"
#cl = get_relevant_concepts_from_dbpedia(query)
qs = ["barrack obama speech white house", "donald trump speech white house"]
training_data = generateTrainingSet(qs)
training_labels = [1, 1, 0, 0]
scaler = preprocessing.StandardScaler().fit(training_data)
train_x_norm = scaler.transform(training_data)
clf = svm.SVC(gamma='scale', decision_function_shape='ovo',kernel='poly')
clf.fit(train_x_norm, training_labels)

