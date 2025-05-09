from rdflib import Graph

# Paths to your TTL files
base_ontology_path = "Ontologies & Dataset/R&S_latest_ontology.ttl"
rdf_data_path = "rdf_generated_data.ttl"
output_path = "merged_for_owl2vec.owl"

# Step 1: Load both TTL files
g = Graph()
print("📥 Loading main ontology...")
g.parse(base_ontology_path, format="turtle")

print("📥 Loading RDF-generated data...")
g.parse(rdf_data_path, format="turtle")

# Step 2: Save the merged graph as RDF/XML (for OWL2Vec*)
print("💾 Saving merged ontology in RDF/XML format...")
g.serialize(destination=output_path, format="pretty-xml")

print(f"\n✅ Done! File created: {output_path}")
