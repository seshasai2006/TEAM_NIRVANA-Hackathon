import xgboost as xgb
import pandas as pd
import numpy as np
import pickle
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# ----------------------------
# Load donor DB and model
# ----------------------------
donors = pd.read_csv("donors_bloodcells.csv")

with open("models/model_bloodcells.pkl", "rb") as f:
    model = pickle.load(f)

# Define sample models for different types
MODELS = {
    "bloodcells": model
}

# ----------------------------
# Example recipient
# ----------------------------
recipient = {
    "A": "A*02:01",
    "B": "B*15:01",
    "C": "C*07:01",
    "DRB1": "DRB1*04:01",
    "DQB1": "DQB1*03:01",
    "blood": "O+",
    "age": 34
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
    rbc = donor["RBC_Count"]
    platelets = donor["Platelet_Count"]
    mcv = donor["MCV"]
    return [blood_match, age_diff, hla_matches, rbc, platelets, mcv]

# ----------------------------
# Predict match scores
# ----------------------------
X = np.array([compute_features(d, recipient) for _, d in donors.iterrows()])
probs = model.predict_proba(X)[:, 1]
donors["MatchScore"] = probs

# ----------------------------
# Top 5 donor matches
# ----------------------------
print("🎯 Top Blood Cell Donor Matches:")
print(donors.sort_values("MatchScore", ascending=False).head(5)[
    ["DonorID", "BloodGroup", "Age", "RBC_Count", "Platelet_Count", "MCV", "MatchScore"]
])

@app.post("/analyze/{sample_type}")
def analyze_sample(sample_type: str, file: UploadFile = File(...)):
    if sample_type not in MODELS:
        raise HTTPException(status_code=400, detail="Invalid sample type")
    try:
        df = pd.read_csv(file.file)
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype('category')
        model = MODELS[sample_type]
        # Use DMatrix with enable_categorical=True for Booster
        dmatrix = xgb.DMatrix(df, enable_categorical=True)
        predictions = model.predict(dmatrix)
        return JSONResponse(content={"predictions": predictions.tolist()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
