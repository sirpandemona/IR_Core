from sklearn import svm, preprocessing
import numpy as np
from pyspotlight import get_relevant_concepts_from_dbpedia


class SVM:
    def __init__(self):
        self.SVM = svm.SVC(gamma='scale', decision_function_shape='ovo', kernel='poly')
        self.scaler = preprocessing.StandardScaler()

    def train(self, data, labels):
        self.scaler = preprocessing.StandardScaler().fit(train_data)
        norm_data = self.scaler.transform(data)
        self.SVM.fit(norm_data, labels)

    def evaluate(self, data) -> np.ndarray:
        norm_data = self.scaler.transform(data)
        labels = self.SVM.predict(norm_data)
        return labels

    @staticmethod
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
                count = count + 1
            rank = rank + 1
            if results.__len__() == 0:
                results = feature_vector
            else:
                results = np.append(results, feature_vector, axis=0)
        return results