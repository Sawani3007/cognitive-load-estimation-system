import streamlit as st
import pandas as pd
import os
import altair as alt
import time
DEPLOY_MODE = True  
DATA_PATH = "sample_log.csv"

st.set_page_config(
    page_title="Cognitive Load Estimation System",
    layout="wide"
)

st.title("🧠 Cognitive Load Estimation System")
st.caption("Live cognitive load monitoring (updates every 60 seconds)")

# ---- AUTO REFRESH (SAFE) ----
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 10:
    st.session_state.last_refresh = time.time()
    st.rerun()

# ---- DATA CHECK ----
if not os.path.exists(DATA_PATH):
    st.error("📷 Camera not running. Start blink_engine.py first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

if df.empty:
    st.warning("⏳ Waiting for first 60-second window...")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"])
latest = df.iloc[-1]

# ---- METRICS ----
col1, col2 = st.columns(2)

col1.metric("Blink Rate (per minute)", latest["blink_rate"])
col2.metric("Cognitive Load", latest["cognitive_load"])

# ---- INTERPRETATION ----
st.markdown("### 🧠 Cognitive Interpretation")

if latest["cognitive_load"] <= 30:
    st.success(
        f"**Normal cognitive load**\n\n"
        f"Typical relaxed baseline ≈ **30**\n\n"
        f"Your value: **{latest['cognitive_load']}**"
    )
elif latest["cognitive_load"] <= 60:
    st.warning(
        f"**Moderate cognitive load**\n\n"
        f"Indicates active thinking or focus\n\n"
        f"Your value: **{latest['cognitive_load']}**"
    )
else:
    st.error(
        f"**High cognitive load**\n\n"
        f"May indicate fatigue or overload\n\n"
        f"Your value: **{latest['cognitive_load']}**"
    )

# ---- GRAPH ----
st.markdown("### 📈 Cognitive Load Trend (Current Session)")

chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("timestamp:T", title="Time"),
    y=alt.Y("cognitive_load:Q", title="Cognitive Load"),
    tooltip=["timestamp:T", "cognitive_load"]
)

st.altair_chart(chart, use_container_width=True)

st.caption(
    f"Last updated: {latest['timestamp']} | "
    f"Blink rate: {latest['blink_rate']}"
)
