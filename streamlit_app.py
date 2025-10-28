"""
Streamlit Demo: Compliance Tracker & Nudge Bot (Enhanced UI Version)
Features:
- Modern CSS styling and embedded JS animations.
- Department dashboard with completion, badges, leaderboard.
- Simulated nudges and predictive risk scoring.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random
import uuid
import textwrap
import streamlit.components.v1 as components

st.set_page_config(page_title="Compliance Tracker & Nudge Bot — Enhanced", layout="wide", page_icon="🤖")

# ----------------------
# CSS Styling (Enhanced)
# ----------------------
st.markdown(
    """
    <style>
    body {background: #f9fafc; font-family: 'Inter', sans-serif;}
    .main-title {font-size: 30px; font-weight: 800; background: linear-gradient(90deg, #3b82f6, #9333ea); -webkit-background-clip: text; color: transparent;}
    .section-title {font-size: 22px; font-weight: 600; color: #374151; margin-top: 20px;}
    .metric-card {background: #ffffff; border-radius: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); padding: 14px 18px; margin-bottom: 10px;}
    .metric-label {font-size: 14px; color: #6b7280;}
    .metric-value {font-size: 22px; font-weight: 700; color: #111827;}
    .badge-gold {background: linear-gradient(90deg,#fbbf24,#f59e0b); padding:2px 8px; border-radius:8px; color:white; font-weight:600;}
    .badge-silver {background: linear-gradient(90deg,#9ca3af,#d1d5db); padding:2px 8px; border-radius:8px; color:white; font-weight:600;}
    .badge-bronze {background: linear-gradient(90deg,#b45309,#92400e); padding:2px 8px; border-radius:8px; color:white; font-weight:600;}
    .stButton>button {background: linear-gradient(90deg,#3b82f6,#6366f1); color:white; font-weight:600; border-radius:8px; border:none; transition:0.3s;}
    .stButton>button:hover {transform: scale(1.05);}
    </style>
    """, unsafe_allow_html=True)

# ----------------------
# JavaScript Enhancements
# ----------------------
js_code = """
<script>
function pulseTitle(){
  const title = window.parent.document.querySelector('.main-title');
  if(title){title.style.transition='0.6s'; title.style.transform='scale(1.05)'; setTimeout(()=>title.style.transform='scale(1)',500);}
}
function notifyUser(msg){
  const note = document.createElement('div');
  note.innerHTML = msg;
  note.style.position='fixed';
  note.style.bottom='20px';
  note.style.right='20px';
  note.style.background='#3b82f6';
  note.style.color='white';
  note.style.padding='10px 18px';
  note.style.borderRadius='8px';
  note.style.boxShadow='0 4px 12px rgba(0,0,0,0.2)';
  note.style.zIndex='9999';
  document.body.appendChild(note);
  setTimeout(()=>note.remove(),3000);
}
</script>
"""
components.html(js_code, height=0)

# ----------------------
# Demo Data
# ----------------------
def create_data():
    random.seed(42)
    depts = ["HR", "Sales", "Finance", "Tech", "Legal"]
    rows = []
    for d in depts:
        for i in range(10):
            rows.append({
                'id': str(uuid.uuid4())[:8],
                'name': f'{d}_Emp_{i+1}',
                'department': d,
                'completed': random.choice([True, False]),
                'points': random.randint(0, 20),
                'due_in_days': random.randint(-20, 60)
            })
    return pd.DataFrame(rows)

df = create_data()

# ----------------------
# UI Layout
# ----------------------
left, mid, right = st.columns([1,2,1])

with mid:
    st.markdown("<div class='main-title'>Compliance Tracker & Nudge Bot — Demo</div>", unsafe_allow_html=True)
    st.markdown("AI Coach that keeps compliance on autopilot. 💡")
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metric-card'><div class='metric-label'>Employees</div><div class='metric-value'>{len(df)}</div></div>", unsafe_allow_html=True)
    completion_rate = (df['completed'].mean() * 100).round(1)
    col2.markdown(f"<div class='metric-card'><div class='metric-label'>Completion Rate</div><div class='metric-value'>{completion_rate}%</div></div>", unsafe_allow_html=True)
    overdue = (df['due_in_days']<0).sum()
    col3.markdown(f"<div class='metric-card'><div class='metric-label'>Overdue</div><div class='metric-value'>{overdue}</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Leaderboard</div>", unsafe_allow_html=True)
    df['badge'] = np.where(df['points']>=15,'<span class="badge-gold">Gold</span>',
                    np.where(df['points']>=8,'<span class="badge-silver">Silver</span>',
                    np.where(df['points']>0,'<span class="badge-bronze">Bronze</span>','')))
    st.markdown(df[['name','department','points','badge']].to_html(escape=False, index=False), unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Simulated Nudge</div>", unsafe_allow_html=True)
    emp = st.selectbox("Choose employee", df['name'])
    if st.button("Send Demo Nudge"):
        st.success(f"Nudge sent to {emp} (simulated)")
        components.html("<script>notifyUser('✅ Nudge sent successfully!'); pulseTitle();</script>", height=0)

with right:
    st.markdown("### Demo Chat")
    q = st.text_input("Ask the bot:")
    if st.button("Send"):
        if any(k in q.lower() for k in ['training','compliance','nudge']):
            st.info("Bot: Remember to review overdue employees weekly and send friendly nudges.")
        else:
            st.warning("No answer related question.")

st.markdown("---")
with st.expander("Developer Notes"):
    st.markdown(textwrap.dedent('''
    - CSS redesigned with gradients and clean cards.
    - JS adds pulse animation and notifications.
    - Confetti could be added on badge awards.
    - Extend this to integrate with Supabase, Slack, or SMTP.
    '''))
