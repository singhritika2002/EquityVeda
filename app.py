import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- PAGE SETUP ---
st.set_page_config(page_title="EquityVeda | India Market Tracker", layout="wide")
st.title("📈 EquityVeda: Real-Time India Market Analysis")
st.markdown("Built by **Your Name** | 2026 Project")

# --- ASSET DATABASE ---
# Expanded list including Indices, Stocks, and Commodities
assets = {
    "Indices": {
        "Nifty 50": "^NSEI",
        "BSE Sensex": "^BSESN",
        "Nifty Bank": "^NSEBANK",
        "Nifty Pharma": "^CNXPHARMA",
        "Nifty 100": "^CNX100",
        "Nifty Next 50": "^NSMIDCP50"
    },
    "Stocks": {
        "Reliance": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Infosys": "INFY.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "SBI": "SBIN.NS",
        "Adani Ent": "ADANIENT.NS",
        "Bharti Airtel": "BHARTIARTL.NS"
    },
    "Commodities": {
        "Gold (MCX)": "GC=F",
        "Silver (MCX)": "SI=F",
        "Crude Oil": "CL=F"
    }
}

# --- SIDEBAR ---
st.sidebar.header("EquityVeda Settings")
category = st.sidebar.selectbox("Select Category", list(assets.keys()))
selected_name = st.sidebar.selectbox("Select Asset", list(assets[category].keys()))
symbol = assets[category][selected_name]

# --- FETCH DATA ---
@st.cache_data(ttl=3600)
def load_data(ticker):
    data = yf.Ticker(ticker)
    df = data.history(period="1mo")
    return df

df = load_data(symbol)

# --- VISUALS ---
if not df.empty:
    current_price = df['Close'].iloc[-1]
    price_change = current_price - df['Close'].iloc[-2]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(f"{selected_name} Price", f"₹{current_price:.2f}", f"{price_change:.2f}")
    
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        name="Market Data"
    )])
    fig.update_layout(title=f"{selected_name} Trend", template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Data not available for this ticker.")

# --- CHAT BOT (ARTHA) ---
st.divider()
st.subheader("💬 Chat with Artha")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm Artha, your EquityVeda assistant. Ask me anything about the markets!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Simple Logic for Artha
    response = f"Artha thinks: You asked about '{prompt}'. Currently, {selected_name} is trading at {current_price:.2f}. Remember to invest wisely!"
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

