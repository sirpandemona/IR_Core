from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore
data_graph = Graph(SPARQLStore("http://dbpedia.org/sparql", context_aware=False))

import time
q3_start_time = time.time()

results = data_graph.query("""
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpo: <http://dbpedia.org/ontology/>

SELECT ?film ?title_fr ?title_en ?actor ?actor_name_fr ?actor_name_en
WHERE {
    {
     SELECT ?film
     WHERE {
        ?film a dbpo:Film ;
              dcterms:subject <http://dbpedia.org/resource/Category:French_films> .
      }
      LIMIT 10
    }
    OPTIONAL {
       ?film rdfs:label ?title_en .
       FILTER langMatches( lang(?title_en), "EN" ) .
    }
    OPTIONAL {
       ?film rdfs:label ?title_fr .
       FILTER langMatches( lang(?title_fr), "FR" ) .
    }
    OPTIONAL {
      ?film dbpo:with ?actor .
      OPTIONAL {
        ?actor foaf:name ?actor_name_en .
        FILTER langMatches( lang(?actor_name_en), "EN" ) .
      }
      OPTIONAL {
        ?actor foaf:name ?actor_name_fr .
        FILTER langMatches( lang(?actor_name_fr), "FR" ) .
      }
    }
}
""")