import pandas as pd
import numpy as np
import pickle

donors = pd.read_csv("donors_blood.csv")

with open("models/model_blood.pkl", "rb") as f:
    model = pickle.load(f)

recipient = {
    "A": "A*01:01",
    "B": "B*08:01",
    "C": "C*04:01",
    "DRB1": "DRB1*15:01",
    "DQB1": "DQB1*02:01",
    "blood": "B+",
    "age": 38
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
    age_diff = abs(donor["Age"] - recipient["age"])
    wbc = donor["WBC_Count"]
    hb = donor["Hemoglobin"]
    return [blood_match, age_diff, hla_matches, wbc, hb]

X = np.array([compute_features(d, recipient) for _, d in donors.iterrows()])
probs = model.predict_proba(X)[:, 1]
donors["MatchScore"] = probs

print("🎯 Top Blood Donor Matches:")
print(donors.sort_values("MatchScore", ascending=False).head(5)[
    ["DonorID", "BloodGroup", "Age", "WBC_Count", "Hemoglobin", "MatchScore"]
])
