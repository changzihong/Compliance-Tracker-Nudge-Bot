# compliance_tracker_demo.py
import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Compliance Tracker & Nudge Bot", layout="wide")

# =========================
# CSS + JS (Toast + Confetti loader)
# =========================
st.markdown(
    """
    <style>
    /* Page */
    body, .stApp { background-color: #e6f7e6 !important; font-family: 'Inter', sans-serif; }

    /* Headings */
    .main-title { color: #044d00; font-weight: 700; font-size: 26px; text-align:center; margin-bottom: 6px; }

    /* White card */
    .white-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        margin-bottom: 18px;
    }

    /* Filters+Summary table stuff */
    .table-card {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        font-size: 14px;
    }
    .table-card th, .table-card td {
        padding: 12px;
        border: 1px solid #e6f7e6;
        text-align: left;
        vertical-align: middle;
        word-wrap: break-word;
    }
    .table-card th {
        background: #f3fff3;
        color: #044d00;
        font-weight: 700;
    }
    .metric-cell {
        text-align: center;
        font-size: 16px;
        font-weight: 700;
        color: #044d00;
    }

    /* table smaller cells for filters */
    .filter-label { width: 18%; min-width: 150px; color:#065f46; font-weight:600; }
    .filter-value { width: 32%; min-width: 200px; }

    /* Toast style (JS will add/remove) */
    .st-toast {
      position: fixed;
      top: 18px;
      right: 18px;
      background: linear-gradient(90deg,#059669,#10b981);
      color: white;
      padding: 10px 16px;
      border-radius: 10px;
      box-shadow: 0 6px 18px rgba(2,6,23,0.2);
      z-index: 10000;
      transform: translateY(-10px);
      opacity: 0;
      transition: all 280ms ease-in-out;
    }
    .st-toast.show { opacity: 1; transform: translateY(0); }

    /* Dataframe fix (Streamlit's internal class may vary; this setting helps) */
    .stDataFrame table { table-layout: fixed; width:100%; }
    .stDataFrame th, .stDataFrame td { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    </style>

    <!-- confetti library (used optionally) -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>

    <script>
    // Show a toast message (title). Auto-hide after 2.4s
    function showToast(message) {
      const existing = document.getElementById('st-custom-toast');
      if (existing) existing.remove();
      const div = document.createElement('div');
      div.id = 'st-custom-toast';
      div.className = 'st-toast';
      div.innerText = message;
      document.body.appendChild(div);
      // trigger show
      setTimeout(()=>div.classList.add('show'), 50);
      setTimeout(()=>{ div.classList.remove('show'); setTimeout(()=>div.remove(),300); }, 2400);
    }

    // small confetti burst
    function confettiBurst() {
      confetti({ particleCount: 40, spread: 60, origin: { y: 0.4 } });
    }
    </script>
    """,
    unsafe_allow_html=True,
)

# =========================
# Demo data
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
# Sidebar (optional quick info)
# =========================
st.sidebar.title("Demo Controls")
st.sidebar.info("This is a Phase-1 demo. Filters update the dashboard below. Press **Apply Filters** to invoke toast + refresh the summary table.")

# =========================
# Page header
# =========================
st.markdown('<div class="main-title">Compliance Tracker & Nudge Bot — Demo</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;color:#065f46;margin-bottom:10px;">AI Coach that keeps compliance on autopilot</div>', unsafe_allow_html=True)

# =========================
# Filters (in white card) and APPLY button triggers JS toast
# =========================
with st.container():
    st.markdown('<div class="white-card">', unsafe_allow_html=True)

    st.markdown("### Filters & Summary", unsafe_allow_html=True)
    # Filter controls (use columns but values will be rendered into the HTML table below)
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        sel_dept = st.multiselect("Department", options=["All"] + departments, default=["HR"])
    with col_b:
        sel_points = st.slider("Points range", 0, 200, (0, 200))
    with col_c:
        sel_badge = st.selectbox("Badge", options=["All", "Gold", "Silver", "Bronze"], index=0)

    # Apply Filters button
    apply_clicked = st.button("Apply Filters")

    # Run JS toast when Apply clicked (via components.html call)
    if apply_clicked:
        # call JS showToast with message
        components.html("<script>showToast('Filters updated successfully!');</script>", height=0)
    st.markdown("<hr style='margin-top:14px;margin-bottom:12px;'>", unsafe_allow_html=True)

    # Compute filtered df
    filtered = df.copy()
    if sel_dept and "All" not in sel_dept:
        filtered = filtered[filtered["Department"].isin(sel_dept)]
    # points range
    filtered = filtered[(filtered["Points"] >= sel_points[0]) & (filtered["Points"] <= sel_points[1])]
    if sel_badge != "All":
        filtered = filtered[filtered["Badge"] == sel_badge]

    # Summary metrics
    avg_completion = filtered["Completion Rate (%)"].mean() if len(filtered) > 0 else 0.0
    total_points = int(filtered["Points"].sum()) if len(filtered) > 0 else 0
    gold_count = len(filtered[filtered["Badge"] == "Gold"])

    # Prepare HTML table (Filters + Summary) - table style card
    sel_dept_display = ", ".join(sel_dept) if sel_dept else "All"
    sel_points_display = f"{sel_points[0]} - {sel_points[1]}"
    sel_badge_display = sel_badge

    table_html = f"""
    <table class="table-card">
      <tr>
        <th class="filter-label">Filter</th>
        <th class="filter-value">Value</th>
        <th class="filter-label">Metric</th>
        <th class="filter-value">Value</th>
      </tr>
      <tr>
        <td><b>Department</b></td>
        <td>{sel_dept_display}</td>
        <td class="metric-cell"><b>Avg Completion</b></td>
        <td class="metric-cell">{avg_completion:.1f}%</td>
      </tr>
      <tr>
        <td><b>Points Range</b></td>
        <td>{sel_points_display}</td>
        <td class="metric-cell"><b>Total Points</b></td>
        <td class="metric-cell">{total_points}</td>
      </tr>
      <tr>
        <td><b>Badge</b></td>
        <td>{sel_badge_display}</td>
        <td class="metric-cell"><b>Gold Members</b></td>
        <td class="metric-cell">{gold_count}</td>
      </tr>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Leaderboard (fixed table)
# =========================
st.markdown('<div class="white-card">', unsafe_allow_html=True)
st.markdown("### 📊 Compliance Leaderboard (Filtered View)")
# display a compact dataframe; use styler to limit index showing
display_df = filtered.reset_index(drop=True)[["Name", "Department", "Completion Rate (%)", "Points", "Badge"]]
# convert badge to colored span for display
def badge_html(b):
    if b == "Gold":
        return '<span style="background:gold;color:#000;padding:4px 8px;border-radius:8px;font-weight:600">Gold</span>'
    if b == "Silver":
        return '<span style="background:silver;color:#000;padding:4px 8px;border-radius:8px;font-weight:600">Silver</span>'
    return '<span style="background:#cd7f32;color:#fff;padding:4px 8px;border-radius:8px;font-weight:600">Bronze</span>'

if not display_df.empty:
    display_df_safe = display_df.copy()
    display_df_safe["Badge"] = display_df_safe["Badge"].apply(badge_html)
    st.markdown(display_df_safe.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("No records match the current filters.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# AI Coach & Nudge Center (white card, full-width)
# =========================
st.markdown('<div class="white-card">', unsafe_allow_html=True)
st.markdown("### 💬 AI Coach & Nudge Center")
col_x, col_y = st.columns([1,1])

with col_x:
    st.subheader("🤖 Chat Demo")
    chat_q = st.text_input("Ask the AI Coach:")
    if st.button("Send Chat"):
        if chat_q.strip() == "":
            st.info("Type a question first.")
        else:
            if any(k in chat_q.lower() for k in ["compliance", "training", "nudge", "policy", "alert"]):
                st.success("🧠 AI Coach: Consider prioritizing employees that are overdue and send friendly nudges.")
                # subtle JS toast as feedback
                components.html("<script>showToast('AI Coach replied');</script>", height=0)
            else:
                st.warning("No answer related question.")

with col_y:
    st.subheader("✉️ Send Nudge (Simulated)")
    if filtered.empty:
        st.info("No employee available to nudge (adjust filters).")
    else:
        recipient = st.selectbox("Select recipient", options=filtered["Name"].tolist())
        training_choice = st.selectbox("Training type", ["Safety Training", "Data Privacy", "Code of Conduct"])
        if st.button("Send Nudge"):
            # simulate send
            st.success(f"✅ Nudge simulated to {recipient} about {training_choice}.")
            # trigger confetti + toast
            components.html("<script>confettiBurst(); showToast('Nudge sent!');</script>", height=0)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("---")
st.caption("Demo — Compliance Tracker & Nudge Bot (Phase 1). Built with Streamlit.")
