# ml/train.py
# Train a crop recommendation model using real-world dataset from /data/crop_data.csv

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from joblib import dump
import os

# ==============================
# Load dataset
# ==============================
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "crop_data.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
print("✅ Loaded dataset successfully!")
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)

# ==============================
# Preprocessing
# ==============================
df.columns = [c.strip().lower() for c in df.columns]

# Expected columns (you can adjust if different)
expected_cols = ["n", "p", "k", "temperature", "humidity", "ph", "rainfall", "label"]
for col in expected_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing required column: {col}")

# Add synthetic features for realism
np.random.seed(42)
df["soil_moisture"] = np.random.uniform(10, 90, len(df))
df["market_signal"] = np.random.choice([0, 1, 2], len(df))
df["yield_q_ha"] = np.random.uniform(150, 400, len(df))

# Define X and targets
X = df[["n", "p", "k", "temperature", "humidity", "ph", "rainfall", "soil_moisture", "market_signal"]]
y_crop = df["label"]
y_yield = df["yield_q_ha"]

# ==============================
# Encode and Scale
# ==============================
le = LabelEncoder()
y_enc = le.fit_transform(y_crop)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ==============================
# Train models
# ==============================
clf = RandomForestClassifier(n_estimators=300, random_state=42)
reg = RandomForestRegressor(n_estimators=300, random_state=42)

clf.fit(X_scaled, y_enc)
reg.fit(X_scaled, y_yield)

# ==============================
# Save models
# ==============================
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")
os.makedirs(OUT_DIR, exist_ok=True)

dump(clf, os.path.join(OUT_DIR, "crop_model.joblib"))
dump(reg, os.path.join(OUT_DIR, "yield_model.joblib"))
dump(scaler, os.path.join(OUT_DIR, "scaler.joblib"))
dump(le, os.path.join(OUT_DIR, "label_encoder.joblib"))

print("🎯 Training complete! Models saved in:", OUT_DIR)
