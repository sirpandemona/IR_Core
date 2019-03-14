from DBPediaRequest import DBPediaRequest
from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import gensim
import warnings
from collections import defaultdict
warnings.simplefilter(action='ignore', category=FutureWarning)


def get_ngrams(text: str) -> list:
    ngram_list = []
    for i in range(1, len(text.split()) + 1):
        n_grams = ngrams(word_tokenize(text), i)
        ngram_list.append([' '.join(grams) for grams in n_grams])
    return ngram_list


def get_candidate_list_using_ngrams(query: str) -> list:
    result_list = []
    ngram_list = get_ngrams(query)
    for ngrams_per_length in ngram_list:
        for ngram in ngrams_per_length:
            try:
                uri = create_uri_from_string(create_uri_from_string(capitalize_all_words(ngram)))
                dbpedia_request = DBPediaRequest(uri)
                if dbpedia_request is not None:
                    result_list.append(dbpedia_request)
            except KeyError:
                # This DBPedia article does not exist
                continue

    return result_list


def rank_candidate_list(query: str, candidate_list: list):
    abstract_list = []
    for candidate in candidate_list:
        abstract_list.append(candidate.get_abstract_of_subject())

    for i in range(0, len(abstract_list)):
        if abstract_list[i] is not None:
            print(candidate_list[i].get_dbpedia_url())

    preprocess_by_tokenizing(query, abstract_list)


def preprocess_by_tokenizing(query: str, abstract_list: list):
    raw_documents = []
    for abstract in abstract_list:
        # If an abstract is none it implies that the found dbpedia page is a redirect page and thus not needed
        if abstract is not None:
            raw_documents.append(abstract)

    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    documents_common_words_removed = [[word for word in document.lower().split() if word not in stoplist]
                  for document in raw_documents]

    # remove words that appear only once
    frequency = defaultdict(int)
    for text in documents_common_words_removed:
        for token in text:
            frequency[token] += 1

    gen_docs = [[token for token in text if frequency[token] > 1]
                  for text in documents_common_words_removed]


    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)

    sims = gensim.similarities.Similarity('', tf_idf[corpus],
                                      num_features=len(dictionary))

    query_doc = [w.lower() for w in word_tokenize(query)]
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]

    print(sims[query_doc_tf_idf])


def capitalize_all_words(s):
    result = ""
    s_list = s.split(' ')
    for word in s_list:
        result = result + word.capitalize() + ' '
    return result.strip()


def create_uri_from_string(subject: str) -> str:
    return subject.replace(' ', '_')
