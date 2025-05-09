import os
import re
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# We will first load the OWL2Vec* vectors from vectors.txt files
def load_vectors(filepath):
    vectors = {}
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:  
            parts = line.strip().split()
            if len(parts) > 2:
                entity = parts[0]
                try:
                    vector = np.array([float(x) for x in parts[1:]])
                    vectors[entity] = vector
                except ValueError:
                    continue
    return vectors

# We will have to normalise entity URIs
def normalize_uri(uri):
    return uri.replace("#", "/")

# Then have the updated load_alignment
def load_alignment(filepath):
    alignments = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "owl:equivalentClass" in line or "owl:equivalentProperty" in line:
                parts = line.replace(".", "").split()
                if len(parts) == 3:
                    source = parts[0].replace("shafi:", "http://www.city.ac.uk/inm713-in3067/2025/Shafi/")
                    target = parts[2].replace("helifit:", "https://opensource.samsung.com/projects/helifit/")
                    alignments.append((source, target))
    return alignments


# Now we will need to match the entities using cosine similarity
def tokenize(entity_iri):
    local_name = entity_iri.split("/")[-1]
    # Here we will split camel case and underscores like this for example: "BodyFat_Measurement" to ["Body", "Fat", "Measurement"]
    tokens = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', local_name)
    return [t.lower() for t in "_".join(tokens).split("_")]

def compute_predictions(vectors1, vectors2, alignment_pairs, threshold=0.4):
    predictions = []
    for e1, e2 in alignment_pairs:
        tokens1 = tokenize(e1)
        tokens2 = tokenize(e2)

        # Now it will try matching every token combination
        for t1 in tokens1:
            for t2 in tokens2:
                if t1 in vectors1 and t2 in vectors2:
                    sim = cosine_similarity([vectors1[t1]], [vectors2[t2]])[0][0]
                    if sim >= threshold:
                        predictions.append((e1, e2))
                        break  # Then it will take the first high-similarity token match
            else:
                continue
            break
    return predictions



# Here we will calculate the precision, the recall and the f1
def evaluate(gold_alignments, predicted_alignments):
    gold_set = set(gold_alignments)
    pred_set = set(predicted_alignments)
    tp = len(gold_set & pred_set)
    precision = tp / len(pred_set) if pred_set else 0
    recall = tp / len(gold_set) if gold_set else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0
    return precision, recall, f1

# Here we will put all the necessary file paths for all the files needed
alignment_file = "alignment.ttl"
vectorsA_file = "OWL2Vec-Star-master/output_configA/vectors.txt"
vectorsB_file = "OWL2Vec-Star-master/output_configB/vectors.txt"

# Then load the data
print("Loading vectors and alignments...")
vectorsA = load_vectors(vectorsA_file)
vectorsB = load_vectors(vectorsB_file)
alignment_pairs = load_alignment(alignment_file)

print("Sample alignments:", alignment_pairs[:5])
print("Sample vector keys (Config A):", list(vectorsA.keys())[:5])
print("Sample vector keys (Config B):", list(vectorsB.keys())[:5])

# This will give the predictions
print("Computing predictions for Config A...")
predictionsA = compute_predictions(vectorsA, vectorsA, alignment_pairs, threshold=0.4)

print("Computing predictions for Config B...")
predictionsB = compute_predictions(vectorsB, vectorsB, alignment_pairs, threshold=0.4)

# This will print evaluation
print("Evaluating Config A...")
precisionA, recallA, f1A = evaluate(alignment_pairs, predictionsA)

print("Evaluating Config B...")
precisionB, recallB, f1B = evaluate(alignment_pairs, predictionsB)

# And finally it will print the results table
results_df = pd.DataFrame({
    "Configuration": ["A", "B"],
    "Precision": [precisionA, precisionB],
    "Recall": [recallA, recallB],
    "F1 Score": [f1A, f1B]
})

print("\n--- Evaluation Results ---")
print(results_df.to_string(index=False))
