import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Compliance Tracker & Nudge Bot", layout="wide")

# =========================
# CSS + JS
# =========================
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #e6f7e6 !important;
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        color: #034d00 !important;
        text-align: center;
    }

    .white-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .summary-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        transition: all 0.5s ease-in-out;
    }

    .summary-table td {
        padding: 10px 15px;
        border: 1px solid #e0f2e0;
        font-size: 15px;
        vertical-align: top;
    }

    .summary-left {
        width: 50%;
        background-color: #f9fff9;
    }

    .summary-right {
        width: 50%;
        background-color: #f9fff9;
    }

    .summary-header {
        background-color: #ccffcc;
        font-weight: 700;
        text-align: center;
        color: #034d00;
    }

    .highlight {
        box-shadow: 0 0 15px rgba(0,128,0,0.4);
        transition: all 0.6s ease-in-out;
    }

    /* Toast styling */
    .st-toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #16a34a;
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        opacity: 0;
        transform: translateY(-15px);
        transition: all 0.4s ease-in-out;
        z-index: 9999;
    }
    .st-toast.show {
        opacity: 1;
        transform: translateY(0);
    }

    /* Center the leaderboard */
    .center-table {
        display: flex;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .center-table table {
        width: 80%;
        border-collapse: collapse;
        table-layout: fixed;
    }
    .center-table th, .center-table td {
        border: 1px solid #d0e6d0;
        padding: 10px;
        text-align: center;
    }
    .center-table th {
        background: #ccffcc;
        color: #034d00;
    }
    </style>

    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    function showToast(msg) {
        const t = document.createElement('div');
        t.className = 'st-toast';
        t.textContent = msg;
        document.body.appendChild(t);
        setTimeout(()=>t.classList.add('show'), 100);
        setTimeout(()=>t.classList.remove('show'), 2200);
        setTimeout(()=>t.remove(), 2600);
    }
    function highlightSummary() {
        const box = document.getElementById('summary-box');
        if (box) {
            box.classList.add('highlight');
            setTimeout(()=>box.classList.remove('highlight'), 1000);
        }
    }
    </script>
    """,
    unsafe_allow_html=True,
)

# =========================
# DATA
# =========================
np.random.seed(42)
departments = ["HR", "Finance", "Operations", "IT", "Legal"]
users = [f"User {i}" for i in range(1, 31)]
data = {
    "Name": users,
    "Department": np.random.choice(departments, size=30),
    "Completion Rate (%)": np.random.randint(50, 100, size=30),
    "Points": np.random.randint(10, 200, size=30),
}
df = pd.DataFrame(data)

def get_badge(points):
    if points >= 150:
        return "Gold"
    elif points >= 80:
        return "Silver"
    else:
        return "Bronze"
df["Badge"] = df["Points"].apply(get_badge)

# =========================
# HEADER
# =========================
st.markdown("## 🧭 Compliance Tracker & Nudge Bot")
st.markdown("<p style='text-align:center;color:#066;'>AI Coach that keeps compliance on autopilot.</p>", unsafe_allow_html=True)

# =========================
# FILTER + SUMMARY
# =========================
st.markdown("### 🎛️ Filter & Summary View")
with st.container():
    st.markdown('<div class="white-card" id="summary-box">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        dept = st.selectbox("Department", ["All"] + departments)
    with col2:
        points_range = st.slider("Points Range", 0, 200, (0, 200))
    with col3:
        badge = st.selectbox("Badge", ["All", "Gold", "Silver", "Bronze"])

    if st.button("Apply Filters"):
        components.html("<script>showToast('Filters refreshed ✅'); highlightSummary();</script>", height=0)

    # Filtered data
    filtered = df.copy()
    if dept != "All":
        filtered = filtered[filtered["Department"] == dept]
    filtered = filtered[(filtered["Points"] >= points_range[0]) & (filtered["Points"] <= points_range[1])]
    if badge != "All":
        filtered = filtered[filtered["Badge"] == badge]

    avg = filtered["Completion Rate (%)"].mean() if len(filtered) > 0 else 0
    total = int(filtered["Points"].sum()) if len(filtered) > 0 else 0
    gold = len(filtered[filtered["Badge"] == "Gold"])

    table_html = f"""
    <table class="summary-table">
        <tr>
            <th class="summary-header">Selected Filters</th>
            <th class="summary-header">Current Summary</th>
        </tr>
        <tr>
            <td class="summary-left">
                <b>Department:</b> {dept}<br>
                <b>Points:</b> {points_range[0]} - {points_range[1]}<br>
                <b>Badge:</b> {badge}
            </td>
            <td class="summary-right">
                <b>Avg Completion:</b> {avg:.1f}%<br>
                <b>Total Points:</b> {total}<br>
                <b>Gold Members:</b> {gold}
            </td>
        </tr>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# LEADERBOARD
# =========================
st.markdown("### 📊 Compliance Leaderboard (Filtered View)")
st.markdown('<div class="white-card">', unsafe_allow_html=True)
display_df = filtered[["Name", "Department", "Completion Rate (%)", "Points", "Badge"]]
if not display_df.empty:
    st.markdown(f"<div class='center-table'>{display_df.to_html(index=False)}</div>", unsafe_allow_html=True)
else:
    st.info("No records match the filters.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CHAT + NUDGE
# =========================
st.markdown("### 💬 AI Coach & Nudge Center")
st.markdown('<div class="white-card">', unsafe_allow_html=True)
colA, colB = st.columns(2)

with colA:
    st.subheader("🤖 Chat Demo")
    msg = st.text_input("Ask the AI Coach:")
    if st.button("Send Message"):
        if any(k in msg.lower() for k in ["policy", "training", "nudge", "alert"]):
            st.success("🧠 AI Coach: Please remind employees to complete upcoming training before the deadline.")
        else:
            st.warning("No answer related question.")

with colB:
    st.subheader("✉️ Send Nudge")
    if filtered.empty:
        st.info("No employee found under current filter.")
    else:
        recipient = st.selectbox("Select Employee", filtered["Name"])
        if st.button("Send Nudge"):
            st.success(f"Nudge sent to {recipient}! (Simulated)")
            components.html("<script>showToast('Nudge sent ✅');</script>", height=0)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 Compliance Tracker & Nudge Bot Demo | HR Department")
