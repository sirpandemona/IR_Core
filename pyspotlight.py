import spotlight
from pprint import pprint


def get_relevant_concepts_from_dbpedia(query: str, confidence: float, support: int) -> list:
    try:
        return spotlight.candidates("http://model.dbpedia-spotlight.org/en/candidates", capitalize_all_words(query),
                                    confidence, support, spotter='Default')
    except spotlight.SpotlightException:
        return [] #nothing found; return empty list


def rank_dbpedia_spotlight_candidates(candidates: list) -> list:
    result_list = []
    for candidate in candidates:
        result_list.append(candidate['resource']['finalScore'])

    return result_list


def print_information_of_dbpedia_concepts(dbpedia_concept_list: list):
    for p in dbpedia_concept_list:
        p.print_all_information_of_subject()


def get_uris(candidates: list) -> list:
    result_list = []
    for candidate in candidates:
        result_list.append(candidate['resource']['uri'])

    return result_list


def capitalize_all_words(s):
    result = ""
    s_list = s.split(' ')
    for word in s_list:
        result = result + word.capitalize() + ' '
    return result.strip()