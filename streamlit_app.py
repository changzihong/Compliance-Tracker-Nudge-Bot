import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(page_title="Compliance Tracker & Nudge Bot", layout="wide")

# =========================
# CUSTOM CSS + JAVASCRIPT
# =========================
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #e6f7e6 !important; /* Light green background */
        font-family: 'Poppins', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #004d00 !important;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }
    .stDataFrame table {
        border-collapse: collapse;
        width: 100%;
        table-layout: fixed;
    }
    .stDataFrame table th, .stDataFrame table td {
        border: 1px solid #b3d9b3;
        padding: 8px;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .stDataFrame table th {
        background-color: #ccffcc;
        color: #004d00;
    }
    .white-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        margin-top: 15px;
    }
    .filter-box {
        background-color: #ccffcc;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .badge {
        border-radius: 12px;
        padding: 5px 10px;
        font-weight: bold;
        color: white;
    }
    .Gold {background-color: gold;}
    .Silver {background-color: silver;}
    .Bronze {background-color: #cd7f32;}
    </style>

    <script>
    function showConfetti() {
        const duration = 2000;
        const end = Date.now() + duration;
        (function frame() {
            confetti({ particleCount: 3, angle: 60, spread: 55, origin: { x: 0 } });
            confetti({ particleCount: 3, angle: 120, spread: 55, origin: { x: 1 } });
            if (Date.now() < end) {
                requestAnimationFrame(frame);
            }
        }());
    }
    </script>
    """,
    unsafe_allow_html=True,
)

# =========================
# DEMO DATA GENERATION
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

# Badge logic
def get_badge(points):
    if points >= 150:
        return "Gold"
    elif points >= 80:
        return "Silver"
    else:
        return "Bronze"

df["Badge"] = df["Points"].apply(get_badge)

# =========================
# FILTERS
# =========================
st.markdown("### 🔍 Filter View", unsafe_allow_html=True)
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        dept_filter = st.selectbox("Department", ["All"] + departments, index=0)
    with col2:
        points_range = st.slider("Points Range", 0, 200, (0, 200))
    with col3:
        badge_filter = st.selectbox("Badge", ["All", "Gold", "Silver", "Bronze"], index=0)

filtered_df = df.copy()

if dept_filter != "All":
    filtered_df = filtered_df[filtered_df["Department"] == dept_filter]

filtered_df = filtered_df[
    (filtered_df["Points"] >= points_range[0]) & (filtered_df["Points"] <= points_range[1])
]

if badge_filter != "All":
    filtered_df = filtered_df[filtered_df["Badge"] == badge_filter]

# =========================
# DISPLAY TABLE
# =========================
st.markdown("### 📊 Compliance Leaderboard")
st.dataframe(
    filtered_df.style.format({"Completion Rate (%)": "{:.0f}%"}).hide(axis="index"),
    use_container_width=True,
)

# =========================
# SUMMARY SECTION
# =========================
st.markdown("### 🧩 Summary Insights")
with st.container():
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Completion Rate", f"{filtered_df['Completion Rate (%)'].mean():.1f}%")
    col2.metric("Total Points", int(filtered_df['Points'].sum()))
    col3.metric("Gold Members", len(filtered_df[filtered_df['Badge'] == 'Gold']))
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CHAT + NUDGE CENTER
# =========================
st.markdown("### 💬 AI Coach & Nudge Center")
with st.container():
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Chat Demo
    with col1:
        st.subheader("🤖 Chat Demo")
        chat_input = st.text_input("Ask the AI Coach something:")
        if chat_input:
            if any(word in chat_input.lower() for word in ["compliance", "training", "nudge", "alert"]):
                st.success("🧠 AI Coach: Please ensure your team completes training by tomorrow! ✅")
            else:
                st.warning("No answer related question.")
        else:
            st.info("Type something to chat with your AI Coach!")

    # Send Nudge Demo
    with col2:
        st.subheader("✉️ Send Nudge Demo")
        recipient = st.selectbox("Select Employee", filtered_df["Name"].unique())
        if st.button("Send Nudge"):
            st.success(f"✅ Nudge sent to {recipient}! (Simulated)")
            st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("© 2025 Compliance Tracker & Nudge Bot (Demo) | Built with Streamlit by HR Team")
