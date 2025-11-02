# import packages
import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.pylabtools import figsize


@st.cache_data
def load_data():
    with open("Mpesa_model.pkl", 'rb') as f:
        data = pickle.load(f)
        return data


combined_data = load_data()

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
        "<div style='display:flex;align-items:center;gap:10px'><div class='logo-circle'>MF</div><div><h3 style='margin:0'>MpesaFinance</h3><div style='font-size:12px;color:gray'>Prophet · Sciki · Explainability</div></div></div>",
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
    st.caption("Built w/ Sklearn + Prophet . prototype")

tabs = st.tabs(["Overview", "Upload & Query", "Insight", "Settings"])

with tabs[0]:
    st.markdown(
        """
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:20px'>
            <div>
                <h1 style='margin:0;background:linear-gradient(90deg,#06b6d4,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
                    MpesaFinance
                </h1>
                <div style='color:gray;font-size:15px;'>AI-powered financial governance</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # --- Stats cards ---
    st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.8, 1, 1, 1])

    with c1:
        st.markdown(
            "<div class='card'><h4 style='margin:0'>What is Mpesa?</h4>"
            "<div style='color:gray;margin-top:6px'>M-Pesa is a mobile money service launched by Safaricom, Kenya’s leading telecommunications company, in 2007. "
            "It has revolutionized financial transactions, allowing users to send, receive, deposit, and withdraw money using their mobile phones. "
            "M-Pesa has played a significant role in financial inclusion, particularly for unbanked populations</div></div>",
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            "<div class='card' style='text-align:center'><h4 style='margin:0'>How M-Pesa Works</h4>"
            "<div style='color:gray;margin-top:6px'>M-Pesa enables users to perform transactions via USSD codes or the M-Pesa app. "
            "Users register with Safaricom and link their mobile numbers to an M-Pesa account.</div></div>",
            unsafe_allow_html=True
        )
    services = [
        "Depositing money at M-Pesa agent shops.",
        "Sending money to other users and non-users.",
        "Withdrawing cash from agents or ATMs.",
        "Merchant payments through Lipa na M-Pesa.",
    ]

    with c3:
        st.markdown(
            f"""
            <div class='card' style='text-align:center'>
                <h4 style='margin:0'>Key Services</h4>
                <div style='color:gray;margin-top:6px'>
                    {' '.join(services)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    challenges = [
        "High transaction costs:Some users find M-Pesa charges expensive",
        "for frequent transactions.less finance monitoring and alert on overspending money"
    ]
    with c4:
        st.markdown(
            f"""
            <div class='card' style='text-align:center'>
                <h4 style='margin:0'>Challenges & risks</h4>
                <div style='color:gray;margin-top:6px'>
                    {' '.join(challenges)}
                </div>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

with tabs[1]:
    st.header("Upload Mpesa statement & run a query")
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Uploaded Mpesa statement", type=["pdf"])
        uploaded_file = BytesIO()
        uploaded_file.seek(0)
        st.success("Mpesa Statement Uploaded - press run query")

        run = st.button("Run Query")
    with col2:
        st.markdown(
            "<div class='card'><h4>How to get Mpesa Statement</h4><ul><li>"
            """You can get an M-Pesa statement by dialing *234#, select "My M-Pesa Information," then "M-Pesa Statement," and follow the prompts to choose a period and enter your email. </li>
            <li>For the app, log in, go to "M-Pesa Services," then "Statements," choose the duration, and export to your email</li><li>We auto-clean text</li></ul></div>""",
            unsafe_allow_html=True)

# on the insight section try making it be a dashboard
with tabs[2]:
    st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)
    r1c1, r1c2, r1c3 = st.columns([5, 5, 5])
    r2c1, r2c2, r2c3 = st.columns([4.5, 4.5, 4.5])
    r3c1, r3c2, r3c3 = st.columns([1.5, 1.5, 1.5])
    r4c1, r4c2, r4c3 = st.columns([1.5, 1.5, 1.5])

    with r1c1:
        st.markdown(
            "<div class='card' style='text-align:center'><h4 style='margin:0'>Balance</h4>"
            "<div style='font-size:28px;font-weight:700;color:#06b6d4'>1 million</div></div>",
            unsafe_allow_html=True
        )
    with r1c2:
        st.markdown(
            "<div class='card' style='text-align:center'><h4 style='margin:0'>Statement Period</h4>"
            "<div style='font-size:28px;font-weight:700;color:#06b6d4'>2025</div></div>",
            unsafe_allow_html=True
        )
    with r1c3:
        st.markdown(
            "<div class='card' style='text-align:center'><h4 style='margin:0'>Statement Period</h4>"
            "<div style='font-size:28px;font-weight:700;color:#06b6d4'>2025</div></div>",
            unsafe_allow_html=True
        )

    with r2c1:
        # Transaction spend
        plt.figure(figsize=(20, 8))
        plt.style.use('seaborn-v0_8-darkgrid')
        plot = sns.barplot(data=combined_data,
                           x='Weekday', y='Transaction_amount', color='#439534', errorbar=None,
                           )
        plt.title('Transaction spend during weekday', fontsize=20)
        plt.xlabel('Weekday', fontsize=20)
        plt.xticks(fontsize=20)
        plt.ylabel('Transaction Amount', fontsize=20)
        plt.yticks(fontsize=20)
        weekday_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        plot.set_xticklabels([weekday_names[i] for i in plot.get_xticks()])
        st.pyplot(plt)

    with r2c2:
        plt.figure(figsize=(20, 8))
        plot = sns.lineplot(data=combined_data, x='Month', y='Transaction_amount', color='#439534', errorbar=None)
        months_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        existing_months = sorted(combined_data['Month'].unique())
        plot.set_xticks(existing_months)
        plot.set_xticklabels([months_names[int(i) - 1] for i in existing_months])
        plot.set_xlim(1, 12)
        plt.title("Monthly Transaction over the Months", fontsize=20)
        plt.xticks(fontsize=20)
        plt.xlabel("Month", fontsize=20)
        plt.ylabel("Transaction Amount", fontsize=20)
        plt.yticks(fontsize=20)
        st.pyplot(plt)

    with r2c3:
        st.write("This is the 2nd row")

    with r3c1:
        st.write("This is the 3rd row")
    with r3c2:
        st.write("This is the 3rd row")
    with r3c3:
        st.write("This is the 3rd row")

    with r4c1:
        st.write("This is the 4th row")
    with r4c2:
        st.write("This is the 4th row")
    with r4c3:
        st.write("This is the 4th row")
