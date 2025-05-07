from rdflib import Graph

# Load your ontology and data
g = Graph()
g.parse("Ontologies & Dataset/R&S_latest_ontology.ttl", format="turtle")
g.parse("Ontologies & Dataset/alignment.ttl", format="turtle")
g.parse("Ontologies & Dataset/rdf_generated_data.ttl", format="turtle")

# --- Query 1: Get all Users and their Age ---
print("\n--- Query 1: Users and Age ---")
q1 = """
PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>

SELECT ?user ?age
WHERE {
  ?user a shafi:User ;
        shafi:Age ?age .
}
"""
for row in g.query(q1):
    print(row)

# --- Query 2: All Yoga Sessions ---
print("\n--- Query 2: Yoga Sessions ---")
q2 = """
PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>

SELECT ?session
WHERE {
  ?session a shafi:Workout_Session ;
           shafi:Workout_Type "Yoga" .
}
"""
for row in g.query(q2):
    print(row)

# --- Query 3: Users with Heart Rate > 100 ---
print("\n--- Query 3: High Heart Rate Users ---")
q3 = """
PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>

SELECT ?user ?rate
WHERE {
  ?user a shafi:User ;
        shafi:Heart_Rate ?rate .
  FILTER(?rate > 100)
}
"""
for row in g.query(q3):
    print(row)
