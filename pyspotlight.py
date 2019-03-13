import spotlight
import requests
from DBPediaRequest import DBPediaRequest
from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.util import ngrams


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


def get_ngrams(text: str) -> list:
    ngram_list = []
    for i in range(1, len(text.split()) + 1):
        n_grams = ngrams(word_tokenize(text), i)
        ngram_list.append([' '.join(grams) for grams in n_grams])
    return ngram_list

def create_uri_from_string(subject: str) -> str:
    return subject.replace(' ', '_')

def get_candidate_list_using_ngrams(query: str) -> list:
    result_list = []
    ngram_list = get_ngrams(query)
    for ngrams_per_length in ngram_list:
        for ngram in ngrams_per_length:
            try:
                uri = create_uri_from_string(create_uri_from_string(capitalize_all_words(ngram)))
                DBPediaRequest(uri)
                result_list.append(uri)
            except KeyError:
                # This DBPedia article does not exist
                continue

    return result_list

def capitalize_all_words(s):
    result = ""
    s_list = s.split(' ')
    for word in s_list:
        result = result + word.capitalize() + ' '
    return result.strip()

# Method 1, using DBPedia spotlight and thus using relevance in the knowledge graph
pprint(get_uris(get_relevant_concepts_from_dbpedia('president obama white house')))

# Method 2, using requests to check if a certain DBPedia page exists and returning it if it does
pprint(get_candidate_list_using_ngrams('president obama white house'))