import pandas as pd
import numpy as np
import pickle

donors = pd.read_csv("donors_saliva.csv")

with open("models/model_saliva.pkl", "rb") as f:
    model = pickle.load(f)

recipient = {
    "A": "A*02:01",
    "B": "B*15:01",
    "C": "C*03:03",
    "DRB1": "DRB1*04:01",
    "DQB1": "DQB1*05:01",
    "blood": "O+"
}

def compute_features(donor, recipient):
    hla_matches = sum([
        donor["Donor_A"] == recipient["A"],
        donor["Donor_B"] == recipient["B"],
        donor["Donor_C"] == recipient["C"],
        donor["Donor_DRB1"] == recipient["DRB1"],
        donor["Donor_DQB1"] == recipient["DQB1"]
    ])
    blood_match = int(donor["BloodGroup"] == recipient["blood"])
    dna_quality = donor["DNA_Quality"]
    contamination = donor["ContaminationFlag"]
    return [blood_match, hla_matches, dna_quality, contamination]

X = np.array([compute_features(d, recipient) for _, d in donors.iterrows()])
probs = model.predict_proba(X)[:, 1]
donors["MatchScore"] = probs

print("🎯 Top Saliva Donor Matches:")
print(donors.sort_values("MatchScore", ascending=False).head(5)[
    ["DonorID", "BloodGroup", "Age", "DNA_Quality", "ContaminationFlag", "MatchScore"]
])
