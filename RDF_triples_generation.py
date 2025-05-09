import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, XSD

def generate_uri(entity_type, data):
    """
    Generate a URI based on the entity type and data.
    """
    if entity_type == "User":
        return shafi[f"User_{data['User ID']}_Age_{data['Age']}"]

    elif entity_type == "Workout":
        return shafi[f"Workout_{data['User ID']}_Calories_{data['Calories Burned']}"]

    elif entity_type == "HealthMetric":
        return shafi[f"HealthMetric_{data['User ID']}_HeartRate_{data['Heart Rate (bpm)']}"]

    elif entity_type == "NutritionPlan":
        return shafi[f"NutritionPlan_{data['User ID']}_Water_{data['Water Intake (liters)']}"]

    else:
        raise ValueError(f"Unknown entity type: {entity_type}")

df = pd.read_csv("C:/Users/Shafi/Documents/GitHub/R-S_Semantics/Ontologies & Dataset/RS_Dataset.csv")

g = Graph()
shafi = Namespace("http://www.city.ac.uk/inm713-in3067/2025/R_S/data/")
g.bind("RS", shafi)

for index, row in df.iterrows():
    user_uri = generate_uri("User", row)
    workout_uri = generate_uri("Workout", row)
    hr_uri = generate_uri("HealthMetric", row)
    nutrition_uri = generate_uri("NutritionPlan", row)
    
    # Define types
    g.add((user_uri, RDF.type, shafi.User))
    g.add((workout_uri, RDF.type, shafi.Workout))
    g.add((hr_uri, RDF.type, shafi.HeartRate))
    g.add((nutrition_uri, RDF.type, shafi.NutritionPlan))

    # Link user to other entities
    g.add((user_uri, shafi.hasWorkout, workout_uri))
    g.add((user_uri, shafi.hasHealthMetric, hr_uri))
    g.add((user_uri, shafi.hasNutritionPlan, nutrition_uri))
   
    # data properties 
    g.add((user_uri, shafi.age, Literal(row['Age'], datatype=XSD.integer)))
    g.add((workout_uri, shafi.caloriesBurned, Literal(row['Calories Burned'], datatype=XSD.float)))
    g.add((hr_uri, shafi.heartRate, Literal(row['Heart Rate (bpm)'], datatype=XSD.integer)))
    g.add((nutrition_uri, shafi.waterIntake, Literal(row['Water Intake (liters)'], datatype=XSD.float)))
    g.add((nutrition_uri, shafi.dailyCaloriesIntake, Literal(row['Daily Calories Intake'], datatype=XSD.float)))
    g.add((workout_uri, shafi.moodBeforeWorkout, Literal(row['Mood Before Workout'], datatype=XSD.string)))
    g.add((workout_uri, shafi.moodAfterWorkout, Literal(row['Mood After Workout'], datatype=XSD.string)))
    

g.serialize(destination="rdf_generated_data.ttl", format="turtle")
for s, p, o in g:
    if "User" in str(s):
        print(f"URI: {s} | Predicate: {p} | Object: {o}")
print("RDF data generated and saved to rdf_generated_data.ttl")