# import packages
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

@st.cache_data
def load_data():
    with open("Mpesa_model.pkl", 'rb') as f:
        data = pickle.load(f)
        return data

st.set_page_config(page_title="MpesaFinancial - Pro", layout="wide", initial_sidebar_state="expanded")

AUTO_THEME_SCRIPT = """
    <script>
(function() {
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const root = document.documentElement;
  if (prefersDark) {
    root.setAttribute('data-theme', 'dark');
  } else {
    root.setAttribute('data-theme', 'light');
  }
})();
</script>
"""

CUSTOM_CSS = r"""
    <style>
:root[data-theme="light"] {
  --bg: #0f172a;
  --card: rgba(255,255,255,0.06);
  --text: #0b1220;
  --accent1: linear-gradient(90deg,#7c3aed, #06b6d4);
}
:root[data-theme="dark"] {
  --bg: #070812;
  --card: rgba(255,255,255,0.04);
  --text: #dbeafe;
  --accent1: linear-gradient(90deg,#06b6d4, #7c3aed);
}

/* Apply glass card effect to streamlit elements */
main .block-container {
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
  padding: 1.6rem 2rem;
}
section[data-testid="stSidebar"] .css-1d391kg {
  background: transparent;
}
.css-1d391kg, .css-1d391kg .stButton button {
  border-radius: 14px;
}

/* Title style */
.header {
  display:flex; align-items:center; gap:12px;
}
.logo-circle {
  width:56px;height:56px;border-radius:12px;
  background: var(--accent1);
  display:flex;align-items:center;justify-content:center;color:white;font-weight:700;
  box-shadow: 0 8px 30px rgba(99,102,241,0.15);
}

/* Card style used in columns */
.card {
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border: 1px solid rgba(255,255,255,0.04);
  padding: 16px;
  border-radius: 12px;
}

/* small pills */
.pill {
  display:inline-block;padding:6px 10px;border-radius:999px;font-size:12px;background:rgba(255,255,255,0.03);
}

/* bot bubble */
.bot {
  background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  padding: 10px 12px;border-radius:12px;margin:6px 0;
}
</style>
"""

st.markdown(AUTO_THEME_SCRIPT, unsafe_allow_html=True)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        "<div style='display:flex;align-items:center;gap:10px'><div class='logo-circle'>JM</div><div><h3 style='margin:0'>JobMatchAI</h3><div style='font-size:12px;color:gray'>NLP · Transformers · Explainability</div></div></div>",
        unsafe_allow_html=True)
    st.markdown("------")
    email = st.text_input("Your email (option)", placeholder="you@example.com")
    st.markdown("**Quick Settings**")
    show_explain = st.checkbox("Show explanation", value=True)

    # --- THEME TOGGLE ---
    st.markdown("### 🌓 Theme")
    st.markdown("""
    <style>
    .toggle-container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(255,255,255,0.04);
      padding: 8px 14px;
      border-radius: 12px;
      margin-top: 6px;
      cursor: pointer;
      font-size: 14px;
    }
    .toggle-switch {
      width: 42px;
      height: 22px;
      background: rgba(255,255,255,0.1);
      border-radius: 999px;
      position: relative;
      transition: all 0.3s ease;
    }
    .toggle-ball {
      width: 18px;
      height: 18px;
      background: white;
      border-radius: 50%;
      position: absolute;
      top: 2px;
      left: 2px;
      transition: all 0.3s ease;
    }
    [data-theme='dark'] .toggle-ball {
      transform: translateX(20px);
      background: linear-gradient(45deg, #06b6d4, #7c3aed);
    }
    </style>
    """, unsafe_allow_html=True)

    # toggle logic
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "auto"

    colA, colB, colC = st.columns([1, 1, 1])
    with colA:
        if st.button("☀️ Light"):
            st.session_state.theme_mode = "light"
    with colB:
        if st.button("🌙 Dark"):
            st.session_state.theme_mode = "dark"
    with colC:
        if st.button("⚙️ Auto"):
            st.session_state.theme_mode = "auto"

    if st.session_state.theme_mode == "light":
        st.markdown("<script>document.documentElement.setAttribute('data-theme', 'light');</script>",
                    unsafe_allow_html=True)
    elif st.session_state.theme_mode == "dark":
        st.markdown("<script>document.documentElement.setAttribute('data-theme', 'dark');</script>",
                    unsafe_allow_html=True)
    else:
        st.markdown(AUTO_THEME_SCRIPT, unsafe_allow_html=True)

    st.markdown("------")
    st.caption("Built w/ spacy + Sentence-Transformers . prototype")

tabs = st.tabs(["Dashboard", "Upload & Query", "Chatbot", "Insight", "Settings"])




