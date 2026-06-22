import numpy as np
import pandas as pd

def optimize_portfolio(historical_prices: pd.DataFrame, investment_amount: float) -> dict:
    if historical_prices.empty or historical_prices.shape[1] < 2:
        return {"error": "Need at least 2 stocks to optimize portfolio."}

    returns = historical_prices.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    num_assets = len(mean_returns)
    num_portfolios = 5000
    
    results = np.zeros((3, num_portfolios))
    weights_record = []
    
    risk_free_rate = 0.02
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        portfolio_return = np.sum(mean_returns * weights) * 252
        
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
        
    max_sharpe_idx = np.argmax(results[2])
    optimal_weights = weights_record[max_sharpe_idx]
    
    allocations = {col: weight * investment_amount for col, weight in zip(returns.columns, optimal_weights)}
    
    return {
        "expected_annual_return": results[0,max_sharpe_idx],
        "annual_volatility": results[1,max_sharpe_idx],
        "sharpe_ratio": results[2,max_sharpe_idx],
        "allocations": allocations,
        "weights": {col: weight for col, weight in zip(returns.columns, optimal_weights)}
    }
