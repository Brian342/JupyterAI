# import packages
import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from io import BytesIO
from Extract_pdf import extract_mpesa_data
from cleaning import *


# @st.cache_data
# def load_data():
#     with open("Mpesa_model.pkl", 'rb') as f:
#         data1 = pickle.load(f)
#         return data1
#
#
# combined_data = load_data()

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
        "<div style='display:flex;align-items:center;gap:10px'><div class='logo-circle'>MF</div><div><h3 style='margin:0'>MpesaFinance</h3><div style='font-size:12px;color:gray'>Prophet · Sklearn · Explainability</div></div></div>",
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
        password = st.text_input("If your PDF is password-protected, enter password:", type="password")

        if uploaded_file is not None:
            st.success("File uploaded successfully!")

            # Step 1: Extract Data
            with st.spinner("Extracting data from your statement and Cleaning It..."):
                df = extract_mpesa_data(uploaded_file, password=password or None)

            if df is not None and not df.empty:
                st.write("### Transactions Extracted:")
                st.dataframe(df.head())

            with st.spinner("cleaning data from your statement ..."):
                st.write('')
                st.write('### Cleaned Statement:')
                data = df.copy()
                data['Paid in'] = data['Paid in'].apply(lambda x: remove_comma(x))
                data['Withdraw\rn'] = data['Withdraw\rn'].apply(lambda x: remove_comma(x))
                data['Balance'] = data['Balance'].apply(lambda x: remove_comma(x))

                # changing the data type
                data = data.astype({
                    'Paid in': float,
                    'Withdraw\rn': float,
                    'Balance': float
                })
                data.drop(columns=['Unnamed: 0'], inplace=True)
                data['Details'] = data['Details'].apply(lambda x: x.replace('\r', ' '))

                details = list(data['Details'].apply(lambda x: transaction(x)).values)
                transactionType = [i[0] for i in details]
                TransactionParty = [i[1] for i in details]

                # formating the time column
                date = data['Completion Time'].apply(lambda x: change_date(x)).values
                Year = [i[0] for i in date]
                Month = [i[1] for i in date]
                Date = [i[2] for i in date]
                Weekday = [i[3] for i in date]
                Hour = [i[4] for i in date]
                Minute = [i[5] for i in date]
                Seconds = [i[6] for i in date]

                transactionDay = []

                reverseDay = Date.copy()[::-1]
                datey = reverseDay[0]

                d = 1

                for i in reverseDay:
                    if i == datey:
                        transactionDay.append(d)
                    else:
                        datey = i
                        d += 1
                        transactionDay.append(d)

                transactionDay.reverse()

                receipt = data['Receipt No'].to_list()
                paid_in = data['Paid in'].fillna('NAN_VALUE').values
                withdraw = list(data['Withdraw\rn'].apply(lambda x: withdrawAmount(x)).values)

                transaction_Data = []

                for i in range(len(paid_in)):
                    try:
                        x = float(paid_in[i])
                        transaction_Data.append((x, 'PAID IN'))
                    except:
                        x = float(withdraw[i])
                        transaction_Data.append((x, 'WITHDRAW'))

                transaction_amount = [i[0] for i in transaction_Data]
                paid_in_or_withdraw = [i[1] for i in transaction_Data]

                balance = data["Balance"].to_list()

                final_data = pd.DataFrame({
                    "Receipt": receipt,
                    "transaction_Day": transactionDay,
                    "Year": Year,
                    "Month": Month,
                    "Date": Date,
                    "Weekday": Weekday,
                    "Hour": Hour,
                    "Minute": Minute,
                    "Seconds": Seconds,
                    "Transaction_type": transactionType,
                    "Transaction_party": TransactionParty,
                    "Transaction_amount": transaction_amount,
                    "paid_in_or_Withdraw": paid_in_or_withdraw,
                    "Balance": balance
                })
                final_data.set_index('Receipt', inplace=True)

                st.dataframe(final_data.head())
                final_data.to_csv("statement_cleaned")
                st.session_state["final_data"] = final_data

    with col2:
        st.markdown(
            "<div class='card'><h4>How to get Mpesa Statement</h4><ul><li>"
            """You can get an M-Pesa statement by dialing *234#, select "My M-Pesa Information," then "M-Pesa Statement," and follow the prompts to choose a period and enter your email. </li>
            <li>For the app, log in, go to "M-Pesa Services," then "Statements," choose the duration, and export to your email</li><li>We auto-clean text</li></ul></div>""",
            unsafe_allow_html=True)

# on the insight section try making it be a dashboard
with tabs[2]:
    if "final_data" in st.session_state:
        final_data = st.session_state["final_data"]
        st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)
        r1c1, r1c2, r1c3 = st.columns([5, 5, 5])
        r2c1, r2c2, r2c3 = st.columns([4.5, 4.5, 4.5])
        r3c1, r3c2, r3c3 = st.columns([1.5, 1.5, 1.5])
        r4c1, r4c2 = st.columns([1.5, 5])
        with r1c1:
            st.markdown(
                "<div class='card' style='text-align:center'><h4 style='margin:0'>Balance</h4>"
                f"<div style='font-size:28px;font-weight:700;color:#06b6d4'>{round(final_data['Balance'].sum())}</div></div>",
                unsafe_allow_html=True

            )
        with r1c2:
            year = final_data['Year'].iloc[0]
            st.markdown(
                "<div class='card' style='text-align:center'><h4 style='margin:0'>Statement Year</h4>"
                f"<div style='font-size:28px;font-weight:700;color:#06b6d4'>{year}</div></div>",
                unsafe_allow_html=True
            )
        with r1c3:
            months = ', '.join(str(y) for y in final_data['Month'].unique())

            st.markdown(
                "<div class='card' style='text-align:center'><h4 style='margin:0'>Statement Month(s)</h4>"
                f"<div style='font-size:28px;font-weight:700;color:#06b6d4'>{months}</div></div>",
                unsafe_allow_html=True
            )

        with r2c1:
            # Transaction spend
            st.markdown(
                "<h5 style='font-size:16px; font-weight:600;'>Transaction spend during weekday</h5>",
                unsafe_allow_html=True
            )
            plt.figure(figsize=(10, 4.8))
            plt.style.use('seaborn-v0_8-darkgrid')
            plot = sns.barplot(data=final_data,
                               x='Weekday', y='Transaction_amount', color='#439534', errorbar=None,
                               )
            plt.xlabel('Weekday', fontsize=0)
            plt.xticks(fontsize=20)
            plt.ylabel('Transaction Amount', fontsize=20)
            plt.yticks(fontsize=20)
            weekday_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            plot.set_xticklabels([weekday_names[i] for i in plot.get_xticks()])
            st.pyplot(plt)
            plt.close()

        with r2c2:
            st.markdown(
                "<h5 style='font-size:16px; font-weight:600;'>Monthly Transaction over the Months</h5>",
                unsafe_allow_html=True
            )
            final_data['Month'] = pd.to_numeric(final_data['Month'], errors='coerce')

            months_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            existing_months = sorted(final_data['Month'].dropna().unique())
            plt.figure(figsize=(10, 5))
            plot = sns.lineplot(
                data=final_data,
                x='Month',
                y='Transaction_amount',
                color='#439534',
                markers='o',
                errorbar=None
            )
            plot.set_xticks(existing_months)
            plot.set_xticklabels([months_names[int(i) - 1] for i in existing_months])

            plot.set_xlim(min(existing_months) - 0.5, max(existing_months) + 0.5)

            plt.xticks(fontsize=20)
            plt.xlabel("Month", fontsize=0)
            plt.ylabel("Transaction Amount", fontsize=20)
            plt.yticks(fontsize=20)
            st.pyplot(plt)
            plt.close()

        with r2c3:
            st.markdown(
                "<h7 style='font-size:16px; font-weight:600;'>Transaction Frequency and Amount by Hour</h7>",
                unsafe_allow_html=True
            )
            fig, ax1 = plt.subplots(figsize=(10, 5.0))
            # Histogram (green)
            sns.histplot(
                data=final_data,
                x='Hour',
                color='#439534',
                binwidth=1,
                alpha=0.7,
                ax=ax1
            )
            ax1.set_ylabel('Number of Transactions per Hour', color='#439534', fontsize=20)
            ax1.tick_params(axis='y', labelcolor='#439534', labelsize=20)
            ax1.set_xlim(0, 23)
            ax1.set_xlabel('Hour', fontsize=20)
            ax1.tick_params(axis='x', labelsize=20)
            # Line plot (red)
            ax2 = ax1.twinx()
            sns.lineplot(
                data=final_data.groupby('Hour')['Transaction_amount'].sum().reset_index(),
                x='Hour',
                y='Transaction_amount',
                color='red',
                linewidth=2.5,
                ax=ax2
            )
            ax2.set_ylabel('Total Transaction Amount', color='red', fontsize=20)
            ax2.tick_params(axis='y', labelcolor='red', labelsize=20)
            # Title and style
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        with r3c1:
            st.markdown(
                "<h5 style='font-size:16px; font-weight:600;'>Daily Transaction where spending spikes</h5>",
                unsafe_allow_html=True
            )
            plt.figure(figsize=(10, 5))
            plot = sns.lineplot(data=final_data, x='Date', y='Transaction_amount', errorbar=None, color='#439534')
            plot.set_xlim(1, 32)
            plt.xticks(fontsize=20)
            plt.xlabel("Date", fontsize=20)
            plt.ylabel("Transaction Amount", fontsize=20)
            plt.yticks(fontsize=20)
            st.pyplot(plt)
            plt.close()

        with r3c2:
            st.markdown(
                "<h5 style='font-size:16px; font-weight:600;'>Most used Transaction Type</h5>",
                unsafe_allow_html=True
            )
            top_10_types = final_data['Transaction_type'].value_counts().nlargest(10).index
            filtered_data = final_data[final_data['Transaction_type'].isin(top_10_types)]
            plt.figure(figsize=(7.8, 6.2))
            sns.countplot(data=filtered_data, y='Transaction_type', color='#439534',
                          order=filtered_data['Transaction_type'].value_counts().index)
            plt.xlabel('Count', fontsize=20)
            plt.xticks(fontsize=17)
            plt.ylabel('Transaction Type', fontsize=0)
            plt.yticks(fontsize=15)
            st.pyplot(plt)
            plt.close()

        with r3c3:
            st.markdown(
                "<h7 style='font-size:16px; font-weight:600;'>Avg Transaction amount by Transaction_type</h7>",
                unsafe_allow_html=True
            )
            top_10_types = final_data['Transaction_type'].value_counts().nlargest(10).index
            filtered_data = final_data[final_data['Transaction_type'].isin(top_10_types)]

            Grouped_avg_type = (filtered_data.groupby('Transaction_type')['Transaction_amount']
                                .mean().sort_values(ascending=False).reset_index())

            plt.figure(figsize=(7.8, 6.2))
            sns.barplot(data=Grouped_avg_type, y='Transaction_type', x='Transaction_amount',
                        order=Grouped_avg_type['Transaction_type'], color='#439534')
            plt.xlabel('Amount', fontsize=20)
            plt.ylabel('Transaction_Type', fontsize=0)
            plt.xticks(fontsize=17)
            plt.yticks(fontsize=15)
            st.pyplot(plt)
            plt.close()

        with r4c1:
            st.markdown(
                "<h5 style='font-size:16px; font-weight:600;'>(Paid In) vs. (Withdraws)</h5>",
                unsafe_allow_html=True
            )
            paid_in = final_data['paid_in_or_Withdraw'].value_counts()
            plt.figure(figsize=(7.8, 6.2))
            fig = go.Figure(go.Pie(labels=paid_in.index, values=paid_in.values, hole=.4,
                                   marker_colors=['#439534', 'red'],
                                   textinfo='percent+label',
                                   hoverinfo='value'))
            fig.update_layout(
                showlegend=False,
                height=450,
            )
            st.plotly_chart(fig, use_container_width=True)
            plt.close()

        with r4c2:
            st.markdown(
                "<h5 style='font-size:16px; font-weight:600;'>Transaction Impact on Account Balance</h5>",
                unsafe_allow_html=True
            )
            plt.figure(figsize=(18, 7))
            Low_balance = 100
            big_transaction = final_data['Transaction_amount'].quantile(.75)

            sns.scatterplot(
                data=final_data, x='Transaction_amount', y='Balance',
                hue=final_data['Transaction_amount'] < Low_balance,
                palette={True: 'red', False: "#439534"},
                style=final_data["Transaction_amount"] > big_transaction,
                markers={True: 'X', False: 'o'},
                size=final_data['Transaction_amount'],
                sizes=(20, 200),
                alpha=0.9
            )
            # Add reference lines
            plt.axvline(big_transaction, color='blue', linestyle='--', label='Big Transaction Threshold')
            plt.axhline(Low_balance, color='red', linestyle='--', label='Low Balance Threshold')

            plt.xlabel('Transaction Amount', fontsize=15)
            plt.ylabel('Account Balance', fontsize=15)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            plt.legend(title='Risk Indicators', bbox_to_anchor=(1.05, 1), loc='upper left')

            #  risk zones
            plt.text(
                x=big_transaction * 1.1,
                y=Low_balance * 0.5,
                s='High Risk Zone',
                color='red',
                fontsize=12,
                bbox=dict(facecolor='white', alpha=0.8)
            )

            plt.tight_layout()
            st.pyplot(plt)
            plt.close()
    else:
        st.warning("Please upload your M-Pesa statement first in the 'Upload & Query' tab.")
