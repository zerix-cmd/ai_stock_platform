import yfinance as yf

def get_fundamental_analysis(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    info = ticker.info

    fundamentals = {
        "pe_ratio": info.get("trailingPE"),
        "pb_ratio": info.get("priceToBook"),
        "roe": info.get("returnOnEquity"),
        "roce": info.get("returnOnEquity"),
        "debt_to_equity": info.get("debtToEquity"),
        "revenue_growth": info.get("revenueGrowth"),
        "profit_growth": info.get("earningsGrowth"),
        "eps": info.get("trailingEps"),
    }
    
    score = 50
    if fundamentals["pe_ratio"] and 0 < fundamentals["pe_ratio"] < 25:
        score += 10
    if fundamentals["roe"] and fundamentals["roe"] > 0.15:
        score += 10
    if fundamentals["debt_to_equity"] and fundamentals["debt_to_equity"] < 100:
        score += 10
    if fundamentals["revenue_growth"] and fundamentals["revenue_growth"] > 0.05:
        score += 10
    if fundamentals["profit_growth"] and fundamentals["profit_growth"] > 0.05:
        score += 10

    fundamentals["fundamental_score"] = min(score, 100)
    return fundamentals
