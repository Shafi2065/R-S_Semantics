import time
import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, XSD, URIRef
from lookup.wikidata import wikidata_lookup

# Load dataset
df = pd.read_csv("C:/Users/Shafi/Documents/GitHub/R-S_Semantics/Ontologies & Dataset/RS_Dataset.csv")

g = Graph()
shafi = Namespace("http://www.city.ac.uk/inm713-in3067/2025/R_S/data/")
g.bind("RS", shafi)
g.bind("wd", "http://www.wikidata.org/entity/")

# Caching for lookups
wikidata_cache = {}

# Lookup limit 
LOOKUP_LIMIT = 10
lookup_count = 0

def cached_wikidata_lookup(term):
    """ Cached lookup for Wikidata """
    global lookup_count

    # Check limit
    if lookup_count >= LOOKUP_LIMIT:
        return None, None

    # Check cache
    if term in wikidata_cache:
        return wikidata_cache[term]

    # Perform lookup
    uri, label = wikidata_lookup(term)

    if uri and "wikidata.org/entity/" in uri:
        wikidata_cache[term] = (uri, label)
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

# Iterate through the dataset
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

            # Wikidata Lookup
            wd_uri, wd_label = cached_wikidata_lookup(term)
            if wd_uri:
                target_uri = {
                    "User": user_uri,
                    "Mood Before Workout": workout_uri,
                    "Mood After Workout": workout_uri
                }[field]
                g.add((target_uri, shafi.hasWikidataLink, URIRef(wd_uri)))

g.serialize(destination="rdf_generated_data_wikidata.ttl", format="turtle")
print(f"RDF data with Wikidata lookup successful. Lookups performed: {lookup_count}/{LOOKUP_LIMIT}")
