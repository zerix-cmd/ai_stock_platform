import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(LSTMModel, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))
        out = self.fc(out[:, -1, :]) 
        return out

def train_and_predict_dl(df: pd.DataFrame, lookback: int = 60):
    if df.empty or len(df) < lookback + 10:
        return {"tomorrow_close": 0.0, "weekly_trend": "Neutral", "monthly_trend": "Neutral"}

    close_prices = df['close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)

    last_sequence = scaled_data[-lookback:]
    last_sequence_tensor = torch.tensor(last_sequence, dtype=torch.float32).unsqueeze(0)

    input_dim = 1
    hidden_dim = 32
    num_layers = 2
    output_dim = 1

    model = LSTMModel(input_dim, hidden_dim, num_layers, output_dim)
    model.eval()

    with torch.no_grad():
        pred = model(last_sequence_tensor)
    
    pred_price = scaler.inverse_transform(pred.numpy())[0][0]
    current_price = df['close'].iloc[-1]
    
    diff = pred_price - current_price
    trend = "Bullish" if diff > 0 else "Bearish" if diff < 0 else "Neutral"

    return {
        "tomorrow_close": float(pred_price),
        "weekly_trend": trend,
        "monthly_trend": trend
    }
