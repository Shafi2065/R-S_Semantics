import numpy as np
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

# Both configuration will be put here as a vector file path and one by one they are tested.
VECTOR_FILE = "OWL2Vec-Star-master/output_configB/vectors.txt"

# First we will load the vectors from the text file
def load_vectors(filepath):
    vectors = {}
    with open(filepath, "r", encoding="utf-8") as f:
        next(f)  # This will skip first line which is the header
        for line in f:
            parts = line.strip().split()
            try:
                if len(parts) > 2:
                    entity = parts[0]
                    vector = np.array([float(x) for x in parts[1:]])
                    vectors[entity] = vector
            except ValueError:
                continue  # And it will also skip lines that can't be parsed
    return vectors


# Now time to calculate the cosine similarity between the two vectors
def cosine_sim(vec1, vec2):
    return cosine_similarity([vec1], [vec2])[0][0]

# Here we will define entity pairs
entity_pairs = [
    ("nutrition", "plan"),           # We expect similarity
    ("heart", "rate"),               # We expect similarity
    ("health", "metric"),            # We expect similarity
    ("user", "calories"),            # We expect dissimilarity
    ("session", "type"),             # We expect dissimilarity
    ("intake", "has")                # We expect dissimilarity
]

# Now we need to load the vectors
vectors = load_vectors(VECTOR_FILE)

# And then Ddsplay the cosine similarities
print("\n--- Cosine Similarity Results ---\n")
for e1, e2 in entity_pairs:
    if e1 in vectors and e2 in vectors:
        sim = cosine_sim(vectors[e1], vectors[e2])
        print(f"{e1:>12} <-> {e2:<12} : {sim:.4f}")
    else:
        print(f"Missing vector for one or both entities:\n  {e1}\n  {e2}")
