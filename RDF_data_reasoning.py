from rdflib import Graph, Namespace, URIRef
from owlrl import DeductiveClosure, OWLRL_Semantics

# Namespaces
SHAFI = Namespace("http://www.city.ac.uk/inm713-in3067/2025/R_S/data/")

# Load ontology and data
g = Graph()
g.parse("Ontologies & Dataset\R&S_latest_ontology.ttl", format="turtle")
g.parse("rdf_generated_data.ttl", format="turtle")

print("\n--- BEFORE REASONING ---")
for s, p, o in g:
    print(s, p, o)

# Apply OWL-RL reasoning
DeductiveClosure(OWLRL_Semantics).expand(g)

print("\n--- AFTER REASONING ---")
for s, p, o in g:
    print(s, p, o)

# Save the inferred graph
g.serialize("rdf_extended_data.ttl", format="turtle")
