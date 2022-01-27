# source: https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples/advanced#List_of_countries_ordered_by_the_number_of_their_cities_with_female_mayor
# List of countries ordered by the number of their cities with female mayor

from SPARQLWrapper import SPARQLWrapper, JSON

# set endpoint
sparql=SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setQuery("""
  #title: Recent events
SELECT ?event ?eventLabel ?date
WHERE
{
  # find events
  ?event wdt:P31/wdt:P279* wd:Q1190554.
  # with a point in time or start date
  OPTIONAL { ?event wdt:P585 ?date. }
  OPTIONAL { ?event wdt:P580 ?date. }
  # but at least one of those
  FILTER(BOUND(?date) && DATATYPE(?date) = xsd:dateTime).
  # not in the future, and not more than 31 days ago
  BIND(NOW() - ?date AS ?distance).
  FILTER(0 <= ?distance && ?distance < 31).
  # and get a label as well
  OPTIONAL {
    ?event rdfs:label ?eventLabel.
    FILTER(LANG(?eventLabel) = "en").
  }
}
# limit to 10 results so we don't timeout
LIMIT 10
""")

sparql.setReturnFormat(JSON)
results=sparql.query().convert()
for result in results["results"]["bindings"]:
    print('{}\t{}\t{}'.format(result["event"]["value"],result["eventLabel"]["value"],result["date"]["value"]))
