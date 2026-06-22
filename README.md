# AI Stock Market Intelligence & Prediction Platform

A production-ready full-stack web application that analyzes stocks, predicts future price direction, ranks investment opportunities, and provides real-time trading insights using Machine Learning, Deep Learning, and traditional Technical/Fundamental analysis.

## Disclaimer
**Stock predictions are probabilistic and markets are unpredictable. This software does not guarantee profits and is not financial advice. Focus on statistical probability, risk management, and backtested performance rather than certainty.**

## Architecture

*   **API Layer:** FastAPI
*   **UI Layer:** Streamlit with Plotly
*   **Data Layer:** SQLAlchemy (PostgreSQL ready, defaults to SQLite), yfinance
*   **Core Modules:** pandas-ta (Technical), yfinance (Fundamental), Mock FinBERT (Sentiment)
*   **Models Layer:** Scikit-learn, XGBoost, LightGBM (ML), PyTorch (LSTM/DL)

## Folder Structure
```text
stock_platform/
├── api/             # FastAPI application and endpoints
├── core/            # Technical, fundamental, sentiment, macro, patterns
├── data/            # SQLAlchemy models, database setup, yfinance fetcher
├── models/          # ML, DL, and Probability engines
├── services/        # Ranking, Portfolio Optimization, Backtesting, Risk
├── ui/              # Streamlit dashboard
└── tests/           # Unit tests
```

## Installation

1. Create a virtual environment and activate it:
   `python3 -m venv venv`
   `source venv/bin/activate`
2. Install requirements:
   `pip install -r requirements.txt`

## Running the Application

You need to run both the FastAPI backend and the Streamlit frontend.

**1. Start FastAPI Backend (API)**
`uvicorn stock_platform.api.main:app --reload`
*API Documentation will be available at: http://127.0.0.1:8000/docs*

**2. Start Streamlit Frontend (UI)**
In a new terminal:
`streamlit run stock_platform/ui/dashboard.py`
*The Dashboard will open in your browser.*

## Database Schema
The database uses SQLAlchemy ORM.
*   `StockInfo`: Stores symbol, company name, sector, industry, exchange.
*   `StockPrice`: Stores historical OHLCV data with timestamp, linked to `StockInfo`.
