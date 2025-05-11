import time
import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, XSD, URIRef
from lookup.wikidata import wikidata_lookup

df = pd.read_csv("C:/Users/Shafi/Documents/GitHub/R-S_Semantics/Ontologies & Dataset/RS_Dataset.csv")
# Create a graph and namespace
g = Graph()
shafi = Namespace("http://www.city.ac.uk/inm713-in3067/2025/R_S/data/")
g.bind("RS", shafi)
g.bind("wd", "http://www.wikidata.org/entity/")

# Caching for Wikidata lookups
wikidata_cache = {}

# Lookup limit configuration
LOOKUP_LIMIT = 10
lookup_count = 0

# Function to perform a cached Wikidata lookup
def cached_wikidata_lookup(term):
    global lookup_count

    # Check if the lookup limit has been reached
    if lookup_count >= LOOKUP_LIMIT:
        return None, None

    # Use the cache if available
    if term in wikidata_cache:
        return wikidata_cache[term]

    # Perform lookup
    uri, label = wikidata_lookup(term)

    # Ensure that only valid Wikidata URIs are returned
    if uri and "wikidata.org/entity/" in uri:
        wikidata_cache[term] = (uri, label)
        lookup_count += 1
        # Add a delay to avoid rate-limiting
        time.sleep(0.5)
        return uri, label

    return None, None

# Function to generate local URIs
def generate_uri(entity_type, data):
    if entity_type == "User":
        return shafi[f"User_{data['User ID']}_Age_{data['Age']}"]
    elif entity_type == "Workout":
        return shafi[f"Workout_{data['User ID']}_Calories_{data['Calories Burned']}"]
    elif entity_type == "HealthMetric":
        return shafi[f"HealthMetric_{data['User ID']}_HeartRate_{data['Heart Rate (bpm)']}"]
    elif entity_type == "NutritionPlan":
        return shafi[f"NutritionPlan_{data['User ID']}_Water_{data['Water Intake (liters)']}"]
    else:
        return None

# Processing the dataset with early exit on lookup limit
for index, row in df.iterrows():
    # Check if lookup limit has been reached
    if lookup_count >= LOOKUP_LIMIT:
        print(f"Lookup limit of {LOOKUP_LIMIT} reached. Terminating further lookups.")
        break

    # Generate local URIs
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

    # Lookup for specific data fields with caching and limit
    fields_to_lookup = ["User", "Mood Before Workout", "Mood After Workout"]
    
    for field in fields_to_lookup:
        # Check limit again before performing the lookup
        if lookup_count >= LOOKUP_LIMIT:
            break

        # Perform lookup only for existing fields
        if field in row:
            term = row[field]
            wikidata_uri, label = cached_wikidata_lookup(term)

            if wikidata_uri:
                # Determine target URI based on field
                target_uri = {
                    "User": user_uri,
                    "Mood Before Workout": workout_uri,
                    "Mood After Workout": workout_uri
                }[field]

                # Add the Wikidata link
                g.add((target_uri, shafi.hasWikidataLink, URIRef(wikidata_uri)))

# Save the RDF graph
g.serialize(destination="rdf_generated_data.ttl", format="turtle")
print(f"RDF data with Wikidata links generated successfully. Lookups performed: {lookup_count}/{LOOKUP_LIMIT}")
