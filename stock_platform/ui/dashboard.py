import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="AI Stock Market Platform", layout="wide")

st.title("📈 AI Stock Market Intelligence & Prediction Platform")
st.markdown("**Disclaimer:** Stock predictions are probabilistic and markets are unpredictable. Focus on statistical probability, risk management, and backtested performance rather than certainty. Not financial advice.")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Portfolio Optimization", "Backtesting"])

symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, RELIANCE.NS)", value="AAPL").upper()

if page == "Dashboard":
    if st.sidebar.button("Analyze"):
        with st.spinner(f"Analyzing {symbol}..."):
            try:
                response = requests.get(f"{API_URL}/analysis/{symbol}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.header(f"{symbol} Analysis Overview")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Latest Price", f"${data['latest_price']:.2f}")
                    col2.metric("Trend Prediction", data['dl_predictions']['weekly_trend'])
                    col3.metric("Buy Probability", f"{data['probabilities']['prob_rise_tomorrow']:.1f}%")
                    col4.metric("Sentiment Score", f"{data['sentiment']['sentiment_score']:.1f}/100")
                    
                    col_left, col_right = st.columns([2, 1])
                    
                    with col_left:
                        st.subheader("Predictions & Probability")
                        p_col1, p_col2 = st.columns(2)
                        with p_col1:
                            st.write("**Directional Probabilities (Tomorrow)**")
                            st.progress(data['probabilities']['prob_rise_tomorrow'] / 100, text=f"Rise: {data['probabilities']['prob_rise_tomorrow']:.1f}%")
                            st.progress(data['probabilities']['prob_fall_tomorrow'] / 100, text=f"Fall: {data['probabilities']['prob_fall_tomorrow']:.1f}%")
                        with p_col2:
                            st.write("**Event Probabilities**")
                            st.write(f"Breakout: {data['probabilities']['prob_breakout']:.1f}%")
                            st.write(f"Reversal: {data['probabilities']['prob_reversal']:.1f}%")
                            
                        st.subheader("Deep Learning Forecast")
                        st.write(f"Tomorrow's Predicted Close: ${data['dl_predictions']['tomorrow_close']:.2f}")
                        st.write(f"Monthly Trend: {data['dl_predictions']['monthly_trend']}")
                        
                    with col_right:
                        st.subheader("Risk Management")
                        risk = data['risk_management']
                        st.write(f"**Stop Loss:** ${risk['stop_loss']:.2f}")
                        st.write(f"**Take Profit:** ${risk['take_profit']:.2f}")
                        st.write(f"**Risk/Reward Ratio:** {risk['risk_reward_ratio']:.2f}")
                        st.write(f"**Suggested Position Size:** {risk['suggested_position_size_shares']:.2f} shares")
                        
                        st.subheader("Detected Patterns")
                        st.write(f"Pattern: {data['patterns']['detected_pattern']}")
                        st.write(f"Confidence: {data['patterns']['pattern_confidence']:.1f}%")

                    st.subheader("Fundamental & Macro Scores")
                    score_col1, score_col2 = st.columns(2)
                    score_col1.metric("Fundamental Strength", f"{data['fundamentals'].get('fundamental_score', 0):.1f}/100")
                    score_col2.metric("Macro Environment", f"{data['macro'].get('macro_score', 0):.1f}/100")

                else:
                    st.error(f"Error fetching data: {response.text}")
            except Exception as e:
                st.error(f"Connection error: Make sure the FastAPI server is running on {API_URL}. Error: {e}")

elif page == "Portfolio Optimization":
    st.header("Portfolio Optimization (MPT)")
    symbols_input = st.text_input("Enter symbols separated by commas", value="AAPL, MSFT, GOOGL")
    amount = st.number_input("Investment Amount ($)", value=10000.0)
    
    if st.button("Optimize"):
        symbols_list = [s.strip() for s in symbols_input.split(",")]
        with st.spinner("Optimizing portfolio..."):
            try:
                response = requests.post(f"{API_URL}/portfolio/optimize?amount={amount}", json=symbols_list)
                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.success("Optimization Complete!")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Expected Annual Return", f"{data['expected_annual_return']*100:.2f}%")
                        col2.metric("Annual Volatility", f"{data['annual_volatility']*100:.2f}%")
                        col3.metric("Sharpe Ratio", f"{data['sharpe_ratio']:.2f}")
                        
                        st.subheader("Optimal Allocations")
                        allocs = data['allocations']
                        fig = go.Figure(data=[go.Pie(labels=list(allocs.keys()), values=list(allocs.values()))])
                        st.plotly_chart(fig)
                else:
                     st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

elif page == "Backtesting":
    st.header("Strategy Backtesting")
    strategy = st.selectbox("Select Strategy", ["SMA_Crossover"])
    
    if st.button("Run Backtest"):
        with st.spinner(f"Running {strategy} on {symbol}..."):
            try:
                response = requests.get(f"{API_URL}/backtest/{symbol}?strategy={strategy}")
                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.subheader("Backtest Results")
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Total Return", f"{data['total_return_pct']:.2f}%")
                        col2.metric("Win Rate", f"{data['win_rate']:.1f}%")
                        col3.metric("Max Drawdown", f"{data['max_drawdown']:.1f}%")
                        col4.metric("Sharpe Ratio", f"{data['sharpe_ratio']:.2f}")
                        
                        st.write(f"**Initial Capital:** ${data['initial_capital']:.2f}")
                        st.write(f"**Final Capital:** ${data['final_capital']:.2f}")
                        st.write(f"**Total Trades:** {data['trades_count']}")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")
