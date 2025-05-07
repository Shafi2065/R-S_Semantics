from rdflib import Graph, Namespace, RDF, URIRef
import pandas as pd

# RDFLib setup
g = Graph()
g.parse(r"C:\\Users\\Shafi\\Documents\\GitHub\\R-S_Semantics\\RDF_generated_data.ttl", format="ttl")

# Define the namespace
shafi = Namespace("http://www.city.ac.uk/inm713-in3067/2025/Shafi/")
g.bind("shafi", shafi)

# SPARQL Query
q = """
PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>

SELECT ?user ?water
WHERE {
    ?user a shafi:User ;
          shafi:hasNutritionPlan ?plan .
    ?plan shafi:waterIntake ?water .
    FILTER(?water < 2.0)
}
"""

# Run the query
results = g.query(q)

# Collect query results into a list
query_results = [(str(row.user), float(row.water)) for row in results]

# Convert to DataFrame
df = pd.DataFrame(query_results, columns=["User", "Water Intake"])

# Export as txt file
output_file = "sparql_query_results.txt"
with open(output_file, "w") as file:
    file.write(df.to_string(index=False))

print(f"Results exported to {output_file}")

