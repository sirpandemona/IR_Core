from pprint import pprint
from pyspotlight import get_relevant_concepts_from_dbpedia, get_uris
from ngramranking import rank_candidate_list, get_candidate_list_using_ngrams

# Method 1, using DBPedia spotlight and thus using relevance in the knowledge graph
#pprint(get_uris(get_relevant_concepts_from_dbpedia('Aspirin cancer prevention')))

# Method 2, using requests to check if a certain DBPedia page exists and returning it if it does
rank_candidate_list('Aspirin cancer prevention', get_candidate_list_using_ngrams('Aspirin cancer prevention'))