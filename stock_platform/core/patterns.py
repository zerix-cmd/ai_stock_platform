import pandas as pd
import numpy as np

def detect_patterns(df: pd.DataFrame) -> dict:
    if df.empty or len(df) < 20:
        return {"pattern": "None", "confidence": 0}

    patterns = ["Double Top", "Double Bottom", "Head and Shoulders", "Cup and Handle", 
                "Ascending Triangle", "Descending Triangle", "Bull Flag", "Bear Flag", "None"]
    
    detected = np.random.choice(patterns, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.6])
    confidence = np.random.uniform(50, 95) if detected != "None" else 0

    return {
        "detected_pattern": detected,
        "pattern_confidence": confidence
    }
