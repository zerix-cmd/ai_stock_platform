from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from stock_platform.data.database import get_db, engine, Base
from stock_platform.data.fetcher import fetch_and_store_data, get_stock_data
from stock_platform.core.technical import calculate_technical_indicators
from stock_platform.core.fundamental import get_fundamental_analysis
from stock_platform.core.sentiment import analyze_news_sentiment
from stock_platform.core.macro import get_macro_indicators
from stock_platform.core.patterns import detect_patterns
from stock_platform.models.ml_models import train_and_predict_ml
from stock_platform.models.dl_models import train_and_predict_dl
from stock_platform.models.probability import calculate_probabilities
from stock_platform.services.ranking import rank_stocks
from stock_platform.services.portfolio import optimize_portfolio
from stock_platform.services.backtesting import run_backtest
from stock_platform.services.risk import calculate_risk_management

app = FastAPI(
    title="AI Stock Market Platform API",
    description="API for Stock Analysis, Prediction, and Portfolio Optimization",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Stock Market Platform API"}

@app.post("/api/v1/data/fetch/{symbol}")
def fetch_data(symbol: str, period: str = "1mo", interval: str = "1d", db: Session = Depends(get_db)):
    fetch_and_store_data(db, symbol, period, interval)
    return {"status": "success", "message": f"Data fetched and stored for {symbol}"}

@app.get("/api/v1/analysis/{symbol}")
def analyze_stock(symbol: str, db: Session = Depends(get_db)):
    df = get_stock_data(db, symbol)
    if df.empty:
        fetch_and_store_data(db, symbol, period="1y")
        df = get_stock_data(db, symbol)
        
    if df.empty:
        raise HTTPException(status_code=404, detail="Data not found for symbol")
        
    tech_df = calculate_technical_indicators(df)
    fundamentals = get_fundamental_analysis(symbol)
    sentiment = analyze_news_sentiment(symbol)
    macro = get_macro_indicators()
    patterns = detect_patterns(tech_df)
    
    ml_preds = train_and_predict_ml(tech_df)
    dl_preds = train_and_predict_dl(tech_df)
    probs = calculate_probabilities(tech_df, ml_preds, patterns)
    
    latest_close = tech_df['close'].iloc[-1]
    latest_atr = tech_df['ATR_14'].iloc[-1] if 'ATR_14' in tech_df.columns else 0.0
    risk = calculate_risk_management(latest_close, latest_atr, dl_preds["weekly_trend"])

    return {
        "symbol": symbol,
        "latest_price": latest_close,
        "technical_signals": {
            "SMA_20": tech_df['SMA_20'].iloc[-1] if 'SMA_20' in tech_df.columns else None,
            "RSI_14": tech_df['RSI_14'].iloc[-1] if 'RSI_14' in tech_df.columns else None,
        },
        "fundamentals": fundamentals,
        "sentiment": sentiment,
        "macro": macro,
        "patterns": patterns,
        "ml_predictions": ml_preds,
        "dl_predictions": dl_preds,
        "probabilities": probs,
        "risk_management": risk,
        "disclaimer": "Predictions are probabilistic and markets are unpredictable. Not financial advice."
    }

@app.post("/api/v1/portfolio/optimize")
def optimize(symbols: List[str], amount: float = 10000.0, db: Session = Depends(get_db)):
    import pandas as pd
    price_data = {}
    for sym in symbols:
        df = get_stock_data(db, sym)
        if df.empty:
            fetch_and_store_data(db, sym, period="1y")
            df = get_stock_data(db, sym)
        if not df.empty:
            price_data[sym] = df['close']
            
    if len(price_data) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 valid symbols with data")
        
    combined_df = pd.DataFrame(price_data)
    result = optimize_portfolio(combined_df, amount)
    return result

@app.get("/api/v1/backtest/{symbol}")
def backtest(symbol: str, strategy: str = "SMA_Crossover", db: Session = Depends(get_db)):
    df = get_stock_data(db, symbol)
    if df.empty:
         fetch_and_store_data(db, symbol, period="2y")
         df = get_stock_data(db, symbol)
         
    tech_df = calculate_technical_indicators(df)
    results = run_backtest(tech_df, strategy)
    return results
