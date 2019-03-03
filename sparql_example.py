from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?craft ?homepage
{
  ?craft foaf:name "Apollo 7" .
  ?craft foaf:homepage ?homepage
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print(results)

for result in results["results"]["bindings"]:
    print(result["label"]["value"])