def get_macro_indicators() -> dict:
    macro_data = {
        "inflation_rate": 3.2,
        "interest_rate": 5.25,
        "gdp_growth": 2.1,
        "currency_strength_dxy": 104.5,
        "unemployment_rate": 3.8
    }

    score = 50
    if macro_data["inflation_rate"] < 4.0: score += 10
    if macro_data["interest_rate"] < 4.0: score += 10
    if macro_data["gdp_growth"] > 2.0: score += 15
    if macro_data["unemployment_rate"] < 5.0: score += 15

    macro_data["macro_score"] = min(score, 100)
    return macro_data
