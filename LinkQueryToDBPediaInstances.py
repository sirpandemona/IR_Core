from DBPediaRequest import DBPediaRequest
from nltk.tokenize import word_tokenize
from nltk.util import ngrams


def get_ngrams(text):
    ngram_list = []
    for i in range(1, len(text.split())+1):
        n_grams = ngrams(word_tokenize(text), i)
        ngram_list.append([ ' '.join(grams) for grams in n_grams])
    return ngram_list


def find_relevant_dbpedia_articles_to_query(query):
    ngram_list = get_ngrams(query)

    for ngram_n_value in ngram_list:
        for ngram in ngram_n_value:
            p = DBPediaRequest(ngram)
            print("Current ngram: " + ngram)
            try:
                p.get_all_information_on_subject()
            except KeyError:
                print("This dbpedia entry does not exist" + "\n")
                continue

find_relevant_dbpedia_articles_to_query('Barack Obama White House')