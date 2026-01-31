import pandas as pd
import numpy as np
import pickle

# ----------------------------
# Load donor DB and model
# ----------------------------
donors = pd.read_csv("donors_tissue.csv")

with open("models/model_tissue.pkl", "rb") as f:
    model = pickle.load(f)

# ----------------------------
# Example recipient
# ----------------------------
recipient = {
    "A": "A*24:02",
    "B": "B*40:01",
    "C": "C*07:01",
    "DRB1": "DRB1*07:01",
    "DQB1": "DQB1*06:03",
    "blood": "A+",
    "age": 45
}

# ----------------------------
# Compute features
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
    viability = donor["ViabilityScore"]
    return [blood_match, age_diff, hla_matches, viability]

# ----------------------------
# Predict probabilities
# ----------------------------
X = np.array([compute_features(d, recipient) for _, d in donors.iterrows()])
probs = model.predict_proba(X)[:, 1]
donors["MatchScore"] = probs

# ----------------------------
# Show top 5 matches
# ----------------------------
print("🎯 Top Tissue Donor Matches:")
print(donors.sort_values("MatchScore", ascending=False).head(5)[
    ["DonorID", "BloodGroup", "Age", "TissueType", "ViabilityScore", "MatchScore"]
])
