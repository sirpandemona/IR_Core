from pprint import pprint
from pyspotlight import get_relevant_concepts_from_dbpedia, get_uris, rank_dbpedia_spotlight_candidates
from ngramranking import rank_candidate_list, get_candidate_list_using_ngrams, get_candidates_with_abstract


# The query
query = 'Cruise ship damage sea life'

# Method 1, using DBPedia spotlight and thus using relevance in the knowledge graph
confidence = 0.2
support = 50
print("Method 1 ranked results:")
pprint(get_uris(get_relevant_concepts_from_dbpedia(query, confidence, support)))
pprint(rank_dbpedia_spotlight_candidates(get_relevant_concepts_from_dbpedia(query, confidence, support)))


# Method 2, using requests to check if a certain DBPedia page exists and returning it if it does
candidate_list = get_candidate_list_using_ngrams(query)
true_candidate_list = get_candidates_with_abstract(candidate_list)
ranks_of_candidates = rank_candidate_list(query, candidate_list)
print("Method 2 ranked results:")
print(true_candidate_list)
print(ranks_of_candidates)