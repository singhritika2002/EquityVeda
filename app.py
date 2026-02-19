import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import google.generativeai as genai

# --- CONFIG & GEMINI SETUP ---
st.set_page_config(page_title="EquityVeda Pro", layout="wide")
# Replace with your actual Gemini API Key from Google AI Studio
genai.configure(api_key="YOUR_ACTUAL_API_KEY")
llm = genai.GenerativeModel('gemini-1.5-flash')

# --- EXPANDED ASSET DATABASE (60+ Assets) ---
assets = {
    "Indices": {
        "Nifty 50": "^NSEI", "BSE Sensex": "^BSESN", "Nifty Bank": "^NSEBANK", "Nifty IT": "^CNXIT",
        "Nifty Pharma": "^CNXPHARMA", "Nifty FMCG": "^CNXFMCG", "Nifty Metal": "^CNXMETAL", 
        "Nifty Auto": "^CNXAUTO", "Nifty Midcap": "^CNXMID", "Nifty Next 50": "^NSMIDCP"
    },
    "Stocks (Nifty 50)": {
        "Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC Bank": "HDFCBANK.NS", "ICICI Bank": "ICICIBANK.NS",
        "Infosys": "INFY.NS", "Bharti Airtel": "BHARTIARTL.NS", "SBI": "SBIN.NS", "L&T": "LT.NS",
        "ITC": "ITC.NS", "HUL": "HINDUNILVR.NS", "Adani Ent": "ADANIENT.NS", "Axis Bank": "AXISBANK.NS",
        "Bajaj Finance": "BAJFINANCE.NS", "Maruti": "MARUTI.NS", "Sun Pharma": "SUNPHARMA.NS", "Titan": "TITAN.NS",
        "Tata Motors": "TATAMOTORS.NS", "ONGC": "ONGC.NS", "NTPC": "NTPC.NS", "JSW Steel": "JSWSTEEL.NS",
        "Asian Paints": "ASIANPAINT.NS", "Kotak Bank": "KOTAKBANK.NS", "Coal India": "COALINDIA.NS", "M&M": "M&M.NS",
        "Tata Steel": "TATASTEEL.NS", "Adani Ports": "ADANIPORTS.NS", "Power Grid": "POWERGRID.NS", "Bajaj Auto": "BAJAJ-AUTO.NS",
        "UltraTech": "ULTRACEMCO.NS", "IndusInd": "INDUSINDBK.NS", "Grasim": "GRASIM.NS", "Hindalco": "HINDALCO.NS",
        "Nestle": "NESTLEIND.NS", "HCL Tech": "HCLTECH.NS", "Tech M": "TECHM.NS", "Wipro": "WIPRO.NS",
        "Cipla": "CIPLA.NS", "Dr. Reddy": "DRREDDY.NS", "Apollo Hosp": "APOLLOHOSP.NS", "Eicher": "EICHERMOT.NS",
        "BPCL": "BPCL.NS", "Britannia": "BRITANNIA.NS", "Divis": "DIVISLAB.NS", "Bajaj Finserv": "BAJAJFINSV.NS",
        "Hero Moto": "HEROMOTOCO.NS", "LTIM": "LTIM.NS", "Shree Cem": "SHREECEM.NS", "UPL": "UPL.NS",
        "Jio Fin": "JIOFIN.NS", "Zomato": "ZOMATO.NS"
    }
}

# --- SIDEBAR & REFRESH ---
st.sidebar.title("Settings")
category = st.sidebar.selectbox("Category", list(assets.keys()))
selected_name = st.sidebar.selectbox("Select Asset", list(assets[category].keys()))
symbol = assets[category][selected_name]

# --- DATA FETCHING (The Fix) ---
@st.cache_data(ttl=60)
def load_data(ticker):
    try:
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)
        # FIX: Flatten MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except: return None

df = load_data(symbol)

# --- DASHBOARD VISUALS ---
if df is not None and not df.empty:
    price = float(df['Close'].iloc[-1])
    st.metric(selected_name, f"₹{price:,.2f}")
    
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- SMART CHATBOT (ARTHA) ---
st.divider()
st.subheader("🤖 Chat with Artha (Powered by Gemini)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display history
for role, text in st.session_state.chat_history:
    st.chat_message(role).write(text)

if prompt := st.chat_input("Ask about any Indian stock..."):
    st.session_state.chat_history.append(("user", prompt))
    st.chat_message("user").write(prompt)
    
    # Artha's Brain: Using Gemini to actually "Talk"
    context = f"Current viewing: {selected_name} at ₹{price:.2f}. "
    full_prompt = f"{context} User asked: {prompt}. Answer as Artha, a helpful market expert."
    
    response = llm.generate_content(full_prompt)
    st.session_state.chat_history.append(("assistant", response.text))
    st.chat_message("assistant").write(response.text)
