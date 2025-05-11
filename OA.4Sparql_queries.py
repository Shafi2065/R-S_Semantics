from rdflib import Graph, Namespace

g = Graph()
g.parse("Ontologies & Dataset/R&S_latest_ontology.ttl", format="turtle")

print(f"Total triples in the graph: {len(g)}")

# This will define the namespace
shafi = Namespace("http://www.city.ac.uk/inm713-in3067/2025/Shafi/")
g.bind("RS", shafi)

# Query 1: For the users and age
print("\n- Query 1: Users and Age -")
q1 = """
PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>

SELECT ?user ?age WHERE {
  ?user a shafi:User ;
        shafi:hasAge ?age .
}
"""
for row in g.query(q1):
    print(row)

# Query 2: For the cardio sessions
print("\n- Query 2: Cardio Sessions -")
q2 = """
PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>
SELECT ?user ?workout
WHERE {
  ?user a shafi:User ;
        shafi:hasWorkout ?workout .
  ?workout shafi:workoutType "Cardio" .
}
"""
for row in g.query(q2):
    print(row)

# Query 3: This is for the high heart rate users (>90)
print("\n- Query 3: High Resting Heart Rate Users (>75) -")
q3 = """
PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>
SELECT ?user ?rate
WHERE {
  ?user a shafi:User ;
        shafi:restingHeartRate ?rate .
  FILTER(xsd:integer(?rate) > 75)
}
"""
for row in g.query(q3):
    print(row)

import csv

# Query 1: Now we will export the users and age which is the 1st query to CSV 
query1 = """
PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>

SELECT ?user ?age WHERE {
    ?user a shafi:User ;
          shafi:hasAge ?age .
}
"""

results1 = g.query(query1)

# This will save it to CSV
with open("query1_users_age.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Age"])
    for row in results1:
        writer.writerow([str(row.user), str(row.age)])

