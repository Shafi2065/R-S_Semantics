from rdflib import Graph, Namespace, RDF, URIRef
import pandas as pd

# RDFLib setup
g = Graph()
g.parse(r"C:\\Users\\Shafi\\Documents\\GitHub\\R-S_Semantics\\RDF_generated_data.ttl", format="ttl")

# Define the namespace
shafi = Namespace("http://www.city.ac.uk/inm713-in3067/2025/Shafi/")
g.bind("shafi", shafi)

# Queries
queries = {
    "query1": """
        PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>
        SELECT ?user ?water
        WHERE {
            ?user a shafi:User ;
                  shafi:hasNutritionPlan ?plan .
            ?plan shafi:waterIntake ?water .
            FILTER(?water < 2.0)
        }
    """,
    "query2": """
        PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>
        SELECT ?user ?moodBeforeWorkout ?moodAfterWorkout
        WHERE {
          ?user shafi:hasWorkout ?workout .
          ?workout shafi:moodBeforeWorkout ?moodBeforeWorkout .
          ?workout shafi:moodAfterWorkout ?moodAfterWorkout .
          FILTER(CONTAINS(LCASE(STR(?moodBeforeWorkout)), "tired"))
        }
    """,
    "query3": """
        PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>
        SELECT ?user
        WHERE {
          {
            ?user shafi:hasWorkout ?w .
            ?w shafi:caloriesBurned ?c .
            FILTER(?c > 600)
          }
          UNION
          {
            ?user shafi:hasWorkout ?w .
            ?w shafi:stepsTaken ?s .
            FILTER(?s > 5000)
          }
          FILTER NOT EXISTS {
            ?user shafi:hasNutritionPlan ?np .
            ?np shafi:sleepHours ?sleep .
            FILTER(?sleep < 5)
          }
        }
    """,
    "query4": """
        PREFIX shafi: <http://www.city.ac.uk/inm713-in3067/2025/Shafi/>
        SELECT ?user (AVG(?calories) AS ?avgCalories) (MIN(?hr) AS ?minHeartRate)
        WHERE {
          ?user a shafi:User ;
                shafi:hasWorkout ?workout ;
                shafi:hasHealthMetric ?metric .
          ?workout shafi:caloriesBurned ?calories .
          ?metric shafi:heartRate ?hr .
        }
        GROUP BY ?user
        HAVING (AVG(?calories) > 500 && MIN(?hr) >= 160)
        ORDER BY DESC(?avgCalories) ASC(?minHeartRate)
    """
}

# Execute each query and write results to a separate file
for query_name, query in queries.items():
    results = g.query(query)

    # Collect query results into a list
    query_results = []
    for row in results:
        # Handle varying number of columns in each query
        query_results.append([str(value) for value in row])

    # Convert to DataFrame
    columns = [str(var) for var in results.vars]
    df = pd.DataFrame(query_results, columns=columns)

    # Export as txt file
    output_file = f"{query_name}_results.txt"
    df.to_csv(output_file, sep="\t", index=False, header=True)
    print(f"Query: {query_name}")

    print(f"Results exported to {output_file}")
