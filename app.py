import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="EquityVeda Pro", layout="wide")
st.title("📈 EquityVeda: Real-Time India Market")

# --- EXPANDED ASSET DATABASE (50 Stocks + 10 Indices) ---
assets = {
    "Indices": {
        "Nifty 50": "^NSEI", "BSE Sensex": "^BSESN", "Nifty Bank": "^NSEBANK", "Nifty IT": "^CNXIT",
        "Nifty Pharma": "^CNXPHARMA", "Nifty Next 50": "^NSMIDCP", "Nifty Midcap 100": "^CNXMID",
        "Nifty FMCG": "^CNXFMCG", "Nifty Metal": "^CNXMETAL", "Nifty Auto": "^CNXAUTO"
    },
    "Stocks": {
        "Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC Bank": "HDFCBANK.NS", "ICICI Bank": "ICICIBANK.NS",
        "Infosys": "INFY.NS", "Bharti Airtel": "BHARTIARTL.NS", "SBI": "SBIN.NS", "Larsen & Toubro": "LT.NS",
        "ITC": "ITC.NS", "Hindustan Unilever": "HINDUNILVR.NS", "Adani Ent": "ADANIENT.NS", "Axis Bank": "AXISBANK.NS",
        "Bajaj Finance": "BAJFINANCE.NS", "Maruti Suzuki": "MARUTI.NS", "Sun Pharma": "SUNPHARMA.NS", "Titan": "TITAN.NS",
        "Tata Motors": "TATAMOTORS.NS", "ONGC": "ONGC.NS", "NTPC": "NTPC.NS", "JSW Steel": "JSWSTEEL.NS",
        "Asian Paints": "ASIANPAINT.NS", "Kotak Bank": "KOTAKBANK.NS", "Coal India": "COALINDIA.NS", "M&M": "M&M.NS",
        "TATA Steel": "TATASTEEL.NS", "Adani Ports": "ADANIPORTS.NS", "Power Grid": "POWERGRID.NS", "Bajaj Auto": "BAJAJ-AUTO.NS",
        "UltraTech Cement": "ULTRACEMCO.NS", "IndusInd Bank": "INDUSINDBK.NS", "Grasim": "GRASIM.NS", "Hindalco": "HINDALCO.NS",
        "Nestle India": "NESTLEIND.NS", "HCL Tech": "HCLTECH.NS", "Tech Mahindra": "TECHM.NS", "Wipro": "WIPRO.NS",
        "Cipla": "CIPLA.NS", "Dr. Reddy's": "DRREDDY.NS", "Apollo Hospitals": "APOLLOHOSP.NS", "Eicher Motors": "EICHERMOT.NS",
        "BPCL": "BPCL.NS", "Britannia": "BRITANNIA.NS", "Divi's Lab": "DIVISLAB.NS", "Bajaj Finserv": "BAJAJFINSV.NS",
        "Hero MotoCorp": "HEROMOTOCO.NS", "LTIMindtree": "LTIM.NS", "Shree Cement": "SHREECEM.NS", "UPL": "UPL.NS",
        "Jio Financial": "JIOFIN.NS", "Zomato": "ZOMATO.NS"
    }
}

# --- SIDEBAR & REFRESH ---
st.sidebar.header("Settings")
category = st.sidebar.selectbox("Category", list(assets.keys()))
selected_name = st.sidebar.selectbox("Select Asset", list(assets[category].keys()))
symbol = assets[category][selected_name]

real_time = st.sidebar.toggle("Real-Time Refresh (1m)", value=False)
if real_time:
    st.info("Refreshing every 60 seconds...")
    st.empty() # Placeholder for rerun logic

# --- SMART DATA FETCH ---
def get_live_data(ticker, period="1mo", interval="1d"):
    try:
        data = yf.download(ticker, period=period, interval=interval, progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except:
        return None

df = get_live_data(symbol)

# --- VISUALS ---
if df is not None and not df.empty:
    current_price = float(df['Close'].iloc[-1])
    change = current_price - float(df['Close'].iloc[-2])
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric(selected_name, f"₹{current_price:,.2f}", f"{change:+.2f}")
    
    with col2:
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Failed to load market data.")

# --- SMART CHATBOT (ARTHA 2.0) ---
st.divider()
st.subheader("🤖 Chat with Artha (Search Enabled)")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ask me about any stock! Try: 'What is the price of Reliance?'"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write

