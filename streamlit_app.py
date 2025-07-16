
import streamlit as st
import json
import datetime
import requests
from pytz import timezone
from threading import Timer

# === CONFIG LOAD ===
with open("config.json") as f:
    config = json.load(f)

alpaca_mode = config.get("ALPACA_MODE", "paper")
live_mode = alpaca_mode.lower() == "live"
mode_label = "🟢 LIVE TRADING" if live_mode else "🧪 PAPER MODE"

# === SIDEBAR ===
st.sidebar.title("⚙️ ScalpX Settings")
st.sidebar.success(f"ScalpX is running in: {mode_label}")

if st.sidebar.button("🔁 Toggle Mode"):
    config["ALPACA_MODE"] = "live" if not live_mode else "paper"
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    st.rerun()

# === DISPLAY HEADER ===
st.title("📈 ScalpX Dashboard")
st.markdown(f"**Mode:** `{alpaca_mode.upper()}`")
st.markdown("---")

# === DISCORD VOICE ALERT ===
def discord_bell_alert():
    webhook_url = config.get("DISCORD_WEBHOOK_URL", "")
    if not webhook_url:
        return
    data = {
        "content": "🔔 **ScalpX is now LIVE!** Market is open. Initiating trade engine...",
        "tts": True
    }
    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        st.error(f"Failed to send Discord alert: {e}")

# === PREMARKET SCAN (using yFinance) ===
def run_premarket_scan():
    import yfinance as yf
    tickers = config.get("WATCHLIST", ["AAPL", "AMD", "TSLA"])
    st.subheader("📊 Premarket Scan (yFinance)")
    for t in tickers:
        data = yf.download(t, period="1d", interval="5m")
        if not data.empty:
            last = data.iloc[-1]
            st.write(f"**{t}**: ${round(last['Close'], 2)}")

# === AUTO SWITCH HANDLER ===
def check_market_open():
    now = datetime.datetime.now(timezone("US/Eastern"))
    return now.hour == 9 and now.minute == 30

def schedule_market_open_switch():
    now = datetime.datetime.now(timezone("US/Eastern"))
    target = now.replace(hour=9, minute=30, second=0, microsecond=0)
    delta = (target - now).total_seconds()
    if delta > 0:
        Timer(delta, switch_to_alpaca).start()

def switch_to_alpaca():
    config["DATA_FEED"] = "alpaca"
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    discord_bell_alert()
    print("🔁 Auto-switched to Alpaca at 9:30 AM.")
    st.rerun()

# === UI INTEGRATION ===
st.subheader("🕘 Trading Schedule Status")
if check_market_open():
    st.success("✅ Market is OPEN — Live trades ready.")
else:
    st.warning("⏳ Market CLOSED — Running yFinance scan.")
    run_premarket_scan()
    schedule_market_open_switch()

# === REPLAY & PERFORMANCE TABS (PLACEHOLDER) ===
st.markdown("---")
st.subheader("📼 Replay / Strategy Preview")
st.info("Live replay engine coming soon...")

st.subheader("📊 Trade Performance")
st.info("P/L tracking and leaderboard dashboard loading...")
