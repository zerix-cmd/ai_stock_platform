def calculate_risk_management(current_price: float, atr: float, expected_trend: str) -> dict:
    if expected_trend == "Bullish":
        stop_loss = current_price - (atr * 1.5)
        take_profit = current_price + (atr * 3.0)
    elif expected_trend == "Bearish":
        stop_loss = current_price + (atr * 1.5)
        take_profit = current_price - (atr * 3.0)
    else:
        stop_loss = current_price - (atr * 1.0)
        take_profit = current_price + (atr * 1.0)
        
    risk = abs(current_price - stop_loss)
    reward = abs(take_profit - current_price)
    rr_ratio = reward / risk if risk > 0 else 0

    capital_at_risk = 10000 * 0.02
    position_size = capital_at_risk / risk if risk > 0 else 0
    
    return {
        "current_price": current_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_reward_ratio": rr_ratio,
        "suggested_position_size_shares": position_size
    }
