import pandas as pd
import numpy as np
import pickle

# ----------------------------
# Load donor DB and model
# ----------------------------
donors = pd.read_csv("donors_bonemarrow.csv")

with open("models/model_bonemarrow.pkl", "rb") as f:
    model = pickle.load(f)

# ----------------------------
# Example recipient
# ----------------------------
recipient = {
    "A": "A*24:02",
    "B": "B*08:01",
    "C": "C*03:03",
    "DRB1": "DRB1*07:01",
    "DQB1": "DQB1*06:03",
    "blood": "B+",
    "age": 41
}

# ----------------------------
# Feature computation
# ----------------------------
def compute_features(donor, recipient):
    hla_matches = sum([
        donor["Donor_A"] == recipient["A"],
        donor["Donor_B"] == recipient["B"],
        donor["Donor_C"] == recipient["C"],
        donor["Donor_DRB1"] == recipient["DRB1"],
        donor["Donor_DQB1"] == recipient["DQB1"]
    ])
    blood_match = int(donor["BloodGroup"] == recipient["blood"])
    age_diff = abs(donor["Age"] - recipient["age"])
    cd34 = donor["CD34_Count"]
    engraftment = donor["EngraftmentScore"]
    viability = donor["ViabilityPercent"]
    return [blood_match, age_diff, hla_matches, cd34, engraftment, viability]

# ----------------------------
# Predict match scores
# ----------------------------
X = np.array([compute_features(d, recipient) for _, d in donors.iterrows()])
probs = model.predict_proba(X)[:, 1]
donors["MatchScore"] = probs

# ----------------------------
# Top 5 donor matches
# ----------------------------
print("🎯 Top Bone Marrow Donor Matches:")
print(donors.sort_values("MatchScore", ascending=False).head(5)[
    ["DonorID", "BloodGroup", "Age", "CD34_Count", "EngraftmentScore", "ViabilityPercent", "MatchScore"]
])
