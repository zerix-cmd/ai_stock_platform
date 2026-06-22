import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

def prepare_features(df: pd.DataFrame):
    df = df.copy()
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
    df.dropna(inplace=True)
    features = df.drop(columns=['target', 'timestamp', 'open', 'high', 'low', 'close', 'volume'], errors='ignore')
    target = df['target']
    return features, target

def train_and_predict_ml(df: pd.DataFrame):
    if df.empty or len(df) < 100:
        return {"buy_probability": 0.5, "sell_probability": 0.5, "expected_return": 0.0, "risk_score": 50}

    X, y = prepare_features(df)
    
    if len(X) < 50:
        return {"buy_probability": 0.5, "sell_probability": 0.5, "expected_return": 0.0, "risk_score": 50}

    latest_features = X.iloc[-1:]
    X_train = X.iloc[:-1]
    y_train = y.iloc[:-1]

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_prob = rf.predict_proba(latest_features)[0][1]

    xgb = XGBClassifier(eval_metric='logloss', random_state=42)
    xgb.fit(X_train, y_train)
    xgb_prob = xgb.predict_proba(latest_features)[0][1]

    lgb = LGBMClassifier(random_state=42)
    lgb.fit(X_train, y_train)
    lgb_prob = lgb.predict_proba(latest_features)[0][1]

    ensemble_prob = float(np.mean([rf_prob, xgb_prob, lgb_prob]))
    expected_return = (ensemble_prob - 0.5) * 2.0
    risk_score = 50 + (abs(0.5 - ensemble_prob) * 100)

    return {
        "buy_probability": ensemble_prob * 100,
        "sell_probability": (1 - ensemble_prob) * 100,
        "expected_return": expected_return,
        "risk_score": min(risk_score, 100)
    }
