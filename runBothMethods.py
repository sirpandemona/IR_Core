from pprint import pprint
from pyspotlight import get_relevant_concepts_from_dbpedia, get_uris
from ngramranking import rank_candidate_list, get_candidate_list_using_ngrams, get_candidates_with_abstract

# Method 1, using DBPedia spotlight and thus using relevance in the knowledge graph
#pprint(get_uris(get_relevant_concepts_from_dbpedia('Aspirin cancer prevention')))

# Method 2, using requests to check if a certain DBPedia page exists and returning it if it does
candidate_list = get_candidate_list_using_ngrams('Aspirin cancer prevention')
true_candidate_list = get_candidates_with_abstract(candidate_list)
ranks_of_candidates = rank_candidate_list('Aspirin cancer prevention', candidate_list)


print(true_candidate_list)
print(ranks_of_candidates)