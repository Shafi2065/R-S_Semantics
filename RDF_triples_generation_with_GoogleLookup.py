import time
import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, XSD, URIRef
from lookup.google import google_lookup


df = pd.read_csv("C:/Users/Shafi/Documents/GitHub/R-S_Semantics/Ontologies & Dataset/RS_Dataset.csv")

g = Graph()
shafi = Namespace("http://www.city.ac.uk/inm713-in3067/2025/R_S/data/")
g.bind("RS", shafi)
g.bind("kg", "https://g.co/kg/")  


google_cache = {}


LOOKUP_LIMIT = 10
lookup_count = 0

def cached_google_lookup(term):
    """ Cached lookup for Google Knowledge Graph """
    global lookup_count

    #
    if lookup_count >= LOOKUP_LIMIT:
        return None, None

    
    if term in google_cache:
        return google_cache[term]

    
    uri, label = google_lookup(term)

    # Ensure that only valid Google KG URIs are returned
    if uri and "kgsearch.googleapis.com" not in uri:
        google_cache[term] = (uri, label)
        lookup_count += 1
        time.sleep(0.5)
        return uri, label

    return None, None

def generate_uri(entity_type, data):
    """ Generate local URIs """
    if entity_type == "User":
        return shafi[f"User_{data['User ID']}_Age_{data['Age']}"]
    elif entity_type == "Workout":
        return shafi[f"Workout_{data['User ID']}_Calories_{data['Calories Burned']}"]
    elif entity_type == "HealthMetric":
        return shafi[f"HealthMetric_{data['User ID']}_HeartRate_{data['Heart Rate (bpm)']}"]
    elif entity_type == "NutritionPlan":
        return shafi[f"NutritionPlan_{data['User ID']}_Water_{data['Water Intake (liters)']}"]
    return None


for index, row in df.iterrows():
    
    if lookup_count >= LOOKUP_LIMIT:
        print(f"Lookup limit of {LOOKUP_LIMIT} reached. Terminating further lookups.")
        break

    # Generate URIs
    user_uri = generate_uri("User", row)
    workout_uri = generate_uri("Workout", row)
    hr_uri = generate_uri("HealthMetric", row)
    nutrition_uri = generate_uri("NutritionPlan", row)

    # Add RDF types
    g.add((user_uri, RDF.type, shafi.User))
    g.add((workout_uri, RDF.type, shafi.Workout))
    g.add((hr_uri, RDF.type, shafi.HeartRate))
    g.add((nutrition_uri, RDF.type, shafi.NutritionPlan))

    # Add data properties
    g.add((user_uri, shafi.age, Literal(row['Age'], datatype=XSD.integer)))
    g.add((workout_uri, shafi.caloriesBurned, Literal(row['Calories Burned'], datatype=XSD.float)))
    g.add((hr_uri, shafi.heartRate, Literal(row['Heart Rate (bpm)'], datatype=XSD.integer)))
    g.add((nutrition_uri, shafi.waterIntake, Literal(row['Water Intake (liters)'], datatype=XSD.float)))

    # Lookup for specific data fields
    fields_to_lookup = ["User", "Mood Before Workout", "Mood After Workout"]
    
    for field in fields_to_lookup:
        if lookup_count >= LOOKUP_LIMIT:
            break

        if field in row:
            term = row[field]

            # Google Lookup
            google_uri, google_label = cached_google_lookup(term)
            if google_uri:
                target_uri = {
                    "User": user_uri,
                    "Mood Before Workout": workout_uri,
                    "Mood After Workout": workout_uri
                }[field]
                g.add((target_uri, shafi.hasGoogleLink, URIRef(google_uri)))

# Serialize the graph
g.serialize(destination="rdf_generated_data_google.ttl", format="turtle")
print(f"RDF data created successfully with Google lookup: {lookup_count}/{LOOKUP_LIMIT}")
