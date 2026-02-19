import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- PAGE SETUP ---
st.set_page_config(page_title="EquityVeda", layout="wide")
st.title("📈 EquityVeda: India Market Analysis")

# --- ASSET DATABASE ---
assets = {
    "Indices": {
        "Nifty 50": "^NSEI", "BSE Sensex": "^BSESN", "Nifty Bank": "^NSEBANK",
        "Nifty Pharma": "^CNXPHARMA", "Nifty IT": "^CNXIT"
    },
    "Stocks": {
        "Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC Bank": "HDFCBANK.NS",
        "Infosys": "INFY.NS", "Tata Motors": "TATAMOTORS.NS"
    },
    "Commodities": {
        "Gold": "GC=F", "Silver": "SI=F"
    }
}

# --- SIDEBAR ---
category = st.sidebar.selectbox("Category", list(assets.keys()))
selected_name = st.sidebar.selectbox("Select Asset", list(assets[category].keys()))
symbol = assets[category][selected_name]

# --- FETCH DATA ---
@st.cache_data(ttl=600) # Caches for 10 mins to avoid Yahoo blocking you
def load_data(ticker):
    try:
        return yf.download(ticker, period="1mo", interval="1d", progress=False)
    except:
        return None

df = load_data(symbol)

# --- VISUALS ---
if df is not None and not df.empty:
    current_price = df['Close'].iloc[-1]
    st.metric(f"{selected_name}", f"₹{current_price:.2f}")
    
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Yahoo Finance is busy. Please refresh in 1 minute.")

# --- CHATBOT (ARTHA) ---
st.divider()
st.subheader("🤖 Chat with Artha")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm Artha. Ask me about Indian markets!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = f"Artha says: You asked about '{prompt}'. {selected_name} is currently at ₹{current_price:.2f}."
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
