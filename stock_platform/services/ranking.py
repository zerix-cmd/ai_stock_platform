def rank_stocks(stocks_data: list) -> dict:
    ranked_list = []
    
    for data in stocks_data:
        tech_score = data.get("technical_score", 50)
        fund_score = data.get("fundamental_score", 50)
        sent_score = data.get("sentiment_score", 50)
        macro_score = data.get("macro_score", 50)
        ai_score = data.get("buy_probability", 50)
        
        total_score = (tech_score * 0.2 + 
                       fund_score * 0.2 + 
                       sent_score * 0.1 + 
                       macro_score * 0.1 + 
                       ai_score * 0.4)
        
        data["total_score"] = total_score
        ranked_list.append(data)
        
    ranked_list.sort(key=lambda x: x["total_score"], reverse=True)
    
    return {
        "top_buy": ranked_list[:10],
        "top_momentum": sorted(ranked_list, key=lambda x: x.get("technical_score", 0), reverse=True)[:10],
        "top_long_term": sorted(ranked_list, key=lambda x: x.get("fundamental_score", 0), reverse=True)[:10],
        "top_undervalued": sorted(ranked_list, key=lambda x: (x.get("fundamental_score", 0) - x.get("total_score", 0)), reverse=True)[:10]
    }
