import spotlight
from pprint import pprint

def get_relevant_concepts_from_dbpedia(query: str) -> list:
    try:
        return spotlight.candidates("http://model.dbpedia-spotlight.org/en/candidates", capitalize_all_words(query),
                                    confidence=0.5, support=20, spotter='Default')
    except spotlight.SpotlightException:
        return [] #nothing found; return empty list


def get_n_resources_with_highest_support(n: int, candidates: list) -> list:
    result_list = []
    contained_uri_list = []
    for candidate in candidates:
        if len(result_list) < n:
            candidate_uri = candidate['resource']['uri']
            if not contained_uri_list.__contains__(candidate_uri):
                result_list.append(candidate)
                contained_uri_list.append(candidate_uri)
        else:
            for entry in result_list:
                current_candidate_support = candidate['resource']['support']
                current_entry_support = entry['resource']['support']
                candidate_uri = candidate['resource']['uri']
                entry_uri = entry['resource']['uri']
                if current_candidate_support > current_entry_support and not contained_uri_list.__contains__(
                        candidate_uri):
                    result_list.remove(entry)
                    contained_uri_list.remove(entry_uri)
                    result_list.append(candidate)
                    contained_uri_list.append(candidate_uri)

    return result_list


def print_information_of_dbpedia_concepts(dbpedia_concept_list: list):
    for p in dbpedia_concept_list:
        p.print_all_information_of_subject()


def get_uris(candidates: list) -> list:
    result_list = []
    for candidate in candidates:
        result_list.append(candidate['resource']['uri'])

    return result_list

# Method 1, using DBPedia spotlight and thus using relevance in the knowledge graph
pprint(get_uris(get_relevant_concepts_from_dbpedia('president obama white house')))

# Method 2, using requests to check if a certain DBPedia page exists and returning it if it does
pprint(get_candidate_list_using_ngrams('president obama white house'))