from rdflib import Graph, RDF, RDFS


# Create a Graph and parse TTL files
g = Graph()
g.parse(r"C:\Users\Shafi\Documents\GitHub\R-S_Semantics\Ontologies & Dataset\RDF_generated_data.ttl", format="ttl")
g.parse(r"C:\Users\Shafi\Documents\GitHub\R-S_Semantics\Ontologies & Dataset\rdf3_googlekg.ttl", format="ttl")
g.parse(r"C:\Users\Shafi\Documents\GitHub\R-S_Semantics\Ontologies & Dataset\rdf3_wikidata.ttl", format="ttl")

for s, p, o in g.triples((None, RDF.type, None)):
    if str(o).startswith("https://schema.org"):
        print(s, p, o)

# SPARQL queries
q = """
PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX schema: <https://schema.org/>

# Query 1: Get all users and their workouts
# SELECT ?user ?workout
# WHERE {
#   ?user a shafi:User ;
#         shafi:hasWorkout ?workout .
# }


# Query 2: Get all workouts with calories burned greater than 500
# SELECT ?workout ?calories
# WHERE {
#   ?workout a shafi:Workout ;
#            shafi:caloriesBurned ?calories .
#   FILTER (?calories > 500)
# }

# Query 3: Get all users with water intake less than 2.0 liters
# SELECT ?user ?water
# WHERE {
#   ?user a shafi:User ;
#         shafi:waterIntake ?water .
#   FILTER (?water < 2.0)
# }

# Query 4: Get all workouts that use specific equipment

# SELECT ?workout ?equipment
# WHERE {
#   ?workout a shafi:Workout ;
#            shafi:performsExerciseWith ?equipment .
# }

# Query 5: Get all users and their activities using Wikidata
# SELECT ?user ?activity
# WHERE {
#   ?user shafi:doesActivity ?activity .
# }

# Query 6: Get all users and their activities using Google Knowledge Graph
# SELECT ?person ?role
# WHERE {
#   ?person a ?role .
#   FILTER(STRSTARTS(STR(?role), "https://schema.org/"))
# }
"""


# Run the query
results = g.query(q)

# Print results
for row in results:
    print(f":Person {row.person}, :Role {row.role}")
    g.serialize(destination="sparql_query_results.csv", format="csv")