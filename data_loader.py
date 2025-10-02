# data_loader.py
import pandas as pd
import os

SAMPLE_PATH = os.path.join(os.path.dirname(__file__), 'sample_data.csv')

def load_nasa_data(path=None):
    if path is None:
        path = SAMPLE_PATH
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        return pd.DataFrame([
            {"id": "SAMPLE-1", "a_km": 1.5e8, "e":0.0167, "incl":0.0, "epoch":"2025-09-16"},
        ])

def generate_sample_data(path=SAMPLE_PATH):
    df = pd.DataFrame({
        "id": ["AST-001","AST-002","AST-003"],
        "diameter_m": [50, 200, 1200],
        "density_kg_m3": [3000, 2600, 2800],
        "velocity_km_s": [11, 20, 25],
        "approach_angle_deg":[30, 45, 60],
        "epoch":["2025-09-16"]*3
    })
    df.to_csv(path, index=False)
    return df
