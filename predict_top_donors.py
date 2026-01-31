# predict_top_donors.py
import pandas as pd
import numpy as np
import pickle 
# Load donors and trained model
donors = pd.read_csv("donors.csv")
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

# Function to compute features
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
    return [blood_match, age_diff, hla_matches]

# Function to predict top donors
def get_top_donors(recipient, top_n=1):
    X_input = np.array([compute_features(donor, recipient) for idx, donor in donors.iterrows()])
    probs = model.predict_proba(X_input)[:, 1]
    donors["MatchProbability"] = probs
    top_donors = donors.sort_values("MatchProbability", ascending=False).head(top_n)
    return top_donors[[
        "DonorID","Donor_A","Donor_B","Donor_C","Donor_DRB1","Donor_DQB1",
        "BloodGroup","Age","Gender","Ethnicity","MatchProbability"
    ]]

# Example usage
if __name__ == "__main__":
    recipient = {
        "A": "A*24:02",
        "B": "B*07:02",
        "C": "C*03:03",
        "DRB1": "DRB1*04:01",
        "DQB1": "DQB1*06:03",
        "blood": "AB+",
        "age": 33
    }

    top_donors = get_top_donors(recipient)
    print("🎯 Top 10 donor matches:")
    print(top_donors)
