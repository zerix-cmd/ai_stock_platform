import pandas as pd
import numpy as np

def calculate_probabilities(df: pd.DataFrame, ml_results: dict, pattern_results: dict) -> dict:
    if df.empty:
        return {
            "prob_rise_tomorrow": 50.0,
            "prob_fall_tomorrow": 50.0,
            "prob_breakout": 10.0,
            "prob_reversal": 10.0
        }

    prob_rise = ml_results.get("buy_probability", 50.0)
    prob_fall = 100 - prob_rise

    pattern = pattern_results.get("detected_pattern", "None")
    confidence = pattern_results.get("pattern_confidence", 0)

    prob_breakout = 10.0
    prob_reversal = 10.0

    if pattern in ["Bull Flag", "Ascending Triangle", "Cup and Handle"]:
        prob_rise += (confidence * 0.1)
        prob_breakout += 40.0
    elif pattern in ["Bear Flag", "Descending Triangle"]:
        prob_fall += (confidence * 0.1)
        prob_breakout += 40.0
    elif pattern in ["Double Bottom"]:
        prob_rise += (confidence * 0.15)
        prob_reversal += 50.0
    elif pattern in ["Double Top", "Head and Shoulders"]:
        prob_fall += (confidence * 0.15)
        prob_reversal += 50.0

    total = prob_rise + prob_fall
    prob_rise = (prob_rise / total) * 100
    prob_fall = (prob_fall / total) * 100

    return {
        "prob_rise_tomorrow": min(max(prob_rise, 0), 100),
        "prob_fall_tomorrow": min(max(prob_fall, 0), 100),
        "prob_breakout": min(max(prob_breakout, 0), 100),
        "prob_reversal": min(max(prob_reversal, 0), 100)
    }
