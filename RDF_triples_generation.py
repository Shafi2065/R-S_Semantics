import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, XSD

df = pd.read_csv("C:/Users/Shafi/Documents/GitHub/R-S_Semantics/Ontologies & Dataset/RS_Dataset.csv")

g = Graph()
shafi = Namespace("http://www.city.ac.uk/inm713-in3067/2025/R_S/data/")
g.bind("RS", shafi)

for index, row in df.iterrows():
    user_id = f"User_{row['User ID']}"
    workout_id = f"Workout_{row['User ID']}"
    hr_id = f"HeartRate_{row['User ID']}"
    nutrition_id = f"NutritionPlan_{row['User ID']}"
    dailycal_id = f"DailyCalories_{row['User ID']}"

    user_uri = shafi[user_id]
    workout_uri = shafi[workout_id]
    hr_uri = shafi[hr_id]
    nutrition_uri = shafi[nutrition_id]
    dailycal_uri = shafi[dailycal_id]

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
print("RDF data generated and saved to rdf_generated_data.ttl")