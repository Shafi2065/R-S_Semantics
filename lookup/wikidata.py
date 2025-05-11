from SPARQLWrapper import SPARQLWrapper, JSON

def wikidata_lookup(term):
    """
    Perform a lookup on Wikidata for a specific term.
    Only returns URIs that start with "http://www.wikidata.org/entity/".
    """
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)

    query = f"""
    SELECT ?item ?itemLabel WHERE {{
      ?item rdfs:label "{term}"@en .
      FILTER STRSTARTS(STR(?item), "http://www.wikidata.org/entity/")
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 1
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    try:
        uri = results["results"]["bindings"][0]["item"]["value"]
        label = results["results"]["bindings"][0]["itemLabel"]["value"]
        return uri, label
    except IndexError:
        return None, None
