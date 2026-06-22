import yfinance as yf
import pandas as pd
from sqlalchemy.orm import Session
from .models import StockInfo, StockPrice
from .database import engine, Base
import datetime
import logging

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

def fetch_and_store_data(db: Session, symbol: str, period: str = "1mo", interval: str = "1d"):
    logger.info(f"Fetching data for {symbol} with period {period} and interval {interval}")
    stock = db.query(StockInfo).filter(StockInfo.symbol == symbol).first()
    
    if not stock:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        stock = StockInfo(
            symbol=symbol,
            company_name=info.get("shortName", symbol),
            sector=info.get("sector", "Unknown"),
            industry=info.get("industry", "Unknown"),
            exchange=info.get("exchange", "Unknown")
        )
        db.add(stock)
        db.commit()
        db.refresh(stock)

    df = yf.download(symbol, period=period, interval=interval, progress=False)
    
    if df.empty:
        logger.warning(f"No data found for {symbol}")
        return
        
    df.reset_index(inplace=True)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if 'Date' in df.columns:
        df.rename(columns={'Date': 'timestamp'}, inplace=True)
    elif 'Datetime' in df.columns:
        df.rename(columns={'Datetime': 'timestamp'}, inplace=True)

    records = []
    for _, row in df.iterrows():
        records.append({
            "stock_id": stock.id,
            "timestamp": row['timestamp'],
            "open": float(row['Open']) if not pd.isna(row['Open']) else None,
            "high": float(row['High']) if not pd.isna(row['High']) else None,
            "low": float(row['Low']) if not pd.isna(row['Low']) else None,
            "close": float(row['Close']) if not pd.isna(row['Close']) else None,
            "volume": float(row['Volume']) if not pd.isna(row['Volume']) else None
        })

    from sqlalchemy.dialects.postgresql import insert as pg_insert
    from sqlalchemy.dialects.sqlite import insert as sqlite_insert
    from .database import DATABASE_URL
    
    insert_stmt = sqlite_insert(StockPrice).values(records)
    if DATABASE_URL.startswith("postgresql"):
        insert_stmt = pg_insert(StockPrice).values(records)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['stock_id', 'timestamp'],
            set_=dict(
                open=insert_stmt.excluded.open,
                high=insert_stmt.excluded.high,
                low=insert_stmt.excluded.low,
                close=insert_stmt.excluded.close,
                volume=insert_stmt.excluded.volume
            )
        )
        db.execute(do_update_stmt)
    else:
        do_ignore_stmt = insert_stmt.on_conflict_do_nothing()
        db.execute(do_ignore_stmt)

    db.commit()

def get_stock_data(db: Session, symbol: str) -> pd.DataFrame:
    stock = db.query(StockInfo).filter(StockInfo.symbol == symbol).first()
    if not stock:
        return pd.DataFrame()
    
    prices = db.query(StockPrice).filter(StockPrice.stock_id == stock.id).order_by(StockPrice.timestamp).all()
    
    if not prices:
        return pd.DataFrame()
        
    df = pd.DataFrame([{
        "timestamp": p.timestamp,
        "open": p.open,
        "high": p.high,
        "low": p.low,
        "close": p.close,
        "volume": p.volume
    } for p in prices])
    
    df.set_index("timestamp", inplace=True)
    return df
