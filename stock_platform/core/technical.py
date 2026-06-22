import pandas as pd
import pandas_ta as ta

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or len(df) < 50:
        return df

    df = df.copy()
    df['SMA_20'] = ta.sma(df['close'], length=20)
    df['SMA_50'] = ta.sma(df['close'], length=50)
    df['EMA_12'] = ta.ema(df['close'], length=12)
    df['EMA_26'] = ta.ema(df['close'], length=26)
    
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    if macd is not None:
        df = pd.concat([df, macd], axis=1)

    df['RSI_14'] = ta.rsi(df['close'], length=14)
    stoch_rsi = ta.stochrsi(df['close'], length=14)
    if stoch_rsi is not None:
        df = pd.concat([df, stoch_rsi], axis=1)

    bbands = ta.bbands(df['close'], length=20, std=2)
    if bbands is not None:
        df = pd.concat([df, bbands], axis=1)
    
    df['ATR_14'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    df['VWAP'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])
    df['OBV'] = ta.obv(df['close'], df['volume'])

    adx = ta.adx(df['high'], df['low'], df['close'], length=14)
    if adx is not None:
        df = pd.concat([df, adx], axis=1)

    df.bfill(inplace=True)
    df.fillna(0, inplace=True)

    return df
