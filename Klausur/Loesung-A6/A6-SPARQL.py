# source: https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples/advanced#List_of_countries_ordered_by_the_number_of_their_cities_with_female_mayor
# List of countries ordered by the number of their cities with female mayor

from SPARQLWrapper import SPARQLWrapper, JSON

# set endpoint
sparql=SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setQuery("""
  SELECT ?element ?elementLabel ?symbol ?number
WHERE
{
?element wdt:P31 wd:Q11344;
wdt:P246 ?symbol;
wdt:P1086 ?number.
SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
}
ORDER BY ?number
""")

sparql.setReturnFormat(JSON)
results=sparql.query().convert()
for result in results["results"]["bindings"]:
    print('{}\t{}\t{}\t{}'.format(result["element"]["value"],result["elementLabel"]["value"],result["symbol"]["value"],result["number"]["value"]))
