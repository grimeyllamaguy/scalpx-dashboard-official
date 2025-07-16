import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="ScalpX Dashboard", layout="wide")

st.title("⚡ ScalpX: Real-Time Trade Command Center")

st.markdown("#### Welcome, Commander Jamal 🧠💰")
st.markdown("_Track, review, and dominate your trades — all in one place._")

# Simulated Data Table
sample_data = {
    "Ticker": ["AAPL", "TSLA", "NVDA", "AMD"],
    "Entry Price": [189.32, 242.56, 121.87, 110.50],
    "Exit Price": [191.20, 245.30, 123.00, 112.10],
    "Result": ["WIN", "WIN", "WIN", "WIN"],
    "Date": [datetime.date.today()] * 4
}
df = pd.DataFrame(sample_data)

st.subheader("📊 Today’s Trades")
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("🧠 _More modules coming soon: Replay Theater, XP system, AI Coach Jamal..._")
