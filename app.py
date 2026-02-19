import streamlit as st
import yfinance as yf
import google.generativeai as genai  # <--- New Library

# 1. SETUP GEMINI (Replace 'YOUR_API_KEY' or use st.secrets)
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash', 
    system_instruction="You are Artha, a witty Indian market expert. Use Hinglish occasionally. Give data-backed insights.")

# --- FETCH DATA FUNCTION ---
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.fast_info
    return f"Current Price of {ticker}: ₹{info['last_price']:.2f}"

# --- CHAT INTERFACE ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display Chat History
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    st.chat_message(role).write(message.parts[0].text)

if prompt := st.chat_input("Ask about Nifty, Reliance, or Market Trends..."):
    st.chat_message("user").write(prompt)
    
    # Generate Response from Gemini
    # We pass the current symbol context to the prompt automatically
    full_prompt = f"Context: The user is currently looking at {selected_name} ({symbol}). User says: {prompt}"
    
    response = st.session_state.chat_session.send_message(full_prompt)
    st.chat_message("assistant").write(response.text)
