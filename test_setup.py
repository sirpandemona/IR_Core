from pprint import pprint
import SVM
import pyspotlight
import pytrec_eval
import json
import scipy
from elasticsearch import Elasticsearch

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

def retrieve_qrels() -> list:
    results = {}
    file = open("qrels.701-850.txt")
    for line in file:
        split_line = line.split(" ")
        qnum = split_line[0]
        docnum = split_line[2]
        relevance = split_line[3]
        if ~(qnum in results):
            results[qnum] = {}
        results[qnum][docnum] =relevance
    return results

def retrieve_Q2A() -> list:
    results = []
    file = open("Q2A-annotation")
    for line in file:
        split_line = line.split(",")
        query = split_line[0]
        article = split_line[1]
        rel = split_line[2]
        results.append(query, article, rel)
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

def retieve_search_results(queries: list) -> list:
    results = []
    for q in queries:   
        (query, num) = q
        res = es.search(index="gov2", body={
            "query":{
                "query_string":{
                    "query": query            
                }
            }
        })
        results.append((query, num, res))
    return results

def reshape_search_results(results: list ) -> dict
    out = {}
    for result in list:
        (query, qnum, res) = result
        out[qnum] = {}
        for hit in res['hits']['hits']:
            rel = hit["_score"]
            docnum = hit["_id"]
            out[qnum][docnum] = rel
    return out

def evaluate_results(results_base: dict, results_wiki: dict, qrels: dict):
    evaluator = pytrec_eval.RelevanceEvaluator(qrels, {'map'})
    eval_base = evaluator.evaluate(results_base)
    eval_wiki = evaluator.evaluate(results_wiki)
    query_ids =  query_ids = list(set(eval_base.keys()) & set(eval_wiki.keys()))
    base_scores = [eval_base[query_id][args.measure] for query_id in query_ids]
    wiki_scores = [wiki_results[query_id][args.measure] for query_id in query_ids]
    sign_test = scipy.stats.ttest_rel(base_scores,wiki_scores)

es = Elasticsearch([{"host":"localhost", "port":"9200"}])
qs = retrieve_queries()
# pprint(qs)
cls = retrieve_concepts(qs)
pprint(cls)
fts = retrieve_features(cls)
pprint(fts)
