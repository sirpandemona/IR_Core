from pprint import pprint

from sklearn import svm, preprocessing
import numpy as np
from pyspotlight import get_relevant_concepts_from_dbpedia
#dummy data
train_x = [[1], [2], [3], [4]]
train_y = [ 0, 0, 1,2]
test_x = [[0], [2.3], [5]]

#training the svm
scaler = preprocessing.StandardScaler().fit(train_x)
train_x_norm = scaler.transform(train_x)
clf = svm.SVC(gamma='scale', decision_function_shape='ovo',kernel='poly')
clf.fit(train_x_norm ,train_y)

#using the svm for classifying unknown objects
test_x_norm = scaler.transform(test_x)
unkw_y = clf.predict(test_x_norm)
print(unkw_y)

def query2feat(query: str) -> np.ndarray:
    concept_list = get_relevant_concepts_from_dbpedia(query)
    rank = 0
    n_rel_art = concept_list.__len__()
    n_feats = 2
    results = np.zeros((n_rel_art,n_feats))
    for candidate in concept_list:
        results[rank, 0] = candidate['resource']['contextualScore']
        results[rank, 1] = candidate['resource']['finalScore']
        rank = rank+1
    return results


pprint(query2feat("obama white house audience"))
