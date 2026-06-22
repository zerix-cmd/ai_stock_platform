import pytest
import pandas as pd
import numpy as np
from stock_platform.core.technical import calculate_technical_indicators
from stock_platform.models.probability import calculate_probabilities
from stock_platform.services.risk import calculate_risk_management

def test_calculate_technical_indicators():
    # Create mock dataframe
    dates = pd.date_range('2023-01-01', periods=60)
    df = pd.DataFrame({
        'open': np.random.rand(60) * 100,
        'high': np.random.rand(60) * 100 + 5,
        'low': np.random.rand(60) * 100 - 5,
        'close': np.random.rand(60) * 100,
        'volume': np.random.randint(1000, 10000, 60)
    }, index=dates)
    
    result = calculate_technical_indicators(df)
    
    # Check if indicators are added
    assert 'SMA_20' in result.columns
    assert 'RSI_14' in result.columns
    assert 'ATR_14' in result.columns
    assert len(result) == 60

def test_calculate_probabilities():
    ml_results = {"buy_probability": 60, "sell_probability": 40}
    pattern_results = {"detected_pattern": "Double Bottom", "pattern_confidence": 80}
    
    # Needs a dummy dataframe, just empty is handled
    df = pd.DataFrame()
    probs = calculate_probabilities(df, ml_results, pattern_results)
    
    # Because df is empty, it should return defaults 50/50
    assert probs["prob_rise_tomorrow"] == 50.0

    # With dummy non-empty
    df2 = pd.DataFrame({'close': [1,2]})
    probs2 = calculate_probabilities(df2, ml_results, pattern_results)
    assert probs2["prob_rise_tomorrow"] > 50.0 # because double bottom should increase it
    assert probs2["prob_reversal"] > 10.0

def test_calculate_risk_management():
    risk = calculate_risk_management(100.0, 2.0, "Bullish")
    assert risk["stop_loss"] == 97.0
    assert risk["take_profit"] == 106.0
    assert risk["risk_reward_ratio"] == 2.0
