from pprint import pprint
import gzip
from html.parser import HTMLParser
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os
import re
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def save_to_ES(text, idx):
    json_obj = {"body": text}
    es.index(index='gov2', doc_type='entry', id=idx, body=json_obj)


def iterate_all_files(root):
    maindirs = os.listdir(root)
    for directory in maindirs:
        subdir = root + "/" + directory
        zips = os.listdir(subdir)
        for zipg in zips:
            ziploc = subdir + "/" + zipg
            with gzip.open(ziploc) as decomp:
                content = decomp.read()
                content_dec = str(content)
                docs = content_dec.split("</DOC>")
                for doc in docs:
                    res = re.search('<DOCNO>(.*)</DOCNO>', doc)
                    if res != None:
                        docnr = res.group(1)
                        dehtml = re.compile('<.*?> ')
                        clean_txt = re.sub(dehtml, ' ', doc)
                        yield {
                            "_index": "gov2",
                            "_id": docnr,
                            "_type": "entry",
                            "doc": {"num": docnr, "txt": clean_txt}
                        }

                       #save_to_ES(clean_txt, docnr)


root = "/media/vasco/Elements/IRData/GOV2/gov2-corpus"
bulk(es, iterate_all_files(root))
