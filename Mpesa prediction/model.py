import pandas as pd

df_model = pd.read_csv("statement_cleaned")
df_model['Date'] = pd.to_datetime(df_model['Date'], errors='coerce')

# keeping only outgoing (spending) transactions
df_model = df_model[df_model['paid_in_or_Withdraw'].str.contains('Withdraw', case=False, na=False)]

# handling missing values
df_model = df_model.dropna(subset=['Transaction_amount', 'Date'])
df_model = df_model[df_model['Transaction_amount'] > 0]

df_model['is_weekend'] = df_model['Weekday'].apply(lambda x: 1 if x >= 5 else 0)
df_model = df_model.sort_values('Date')
df_model['rolling_avg_spent'] = df_model['Transaction_amount'].rolling(window=7, min_periods=1).mean()


# transaction time category
def time_group(h):
    if 5 <= h <= 12:
        return 'Morning'
    elif 12 <= h <= 18:
        return 'Afternoon'
    else:
        return 'Night'


df_model['time_period'] = df_model['Hour'].apply(time_group)

# Agg Daily Spending's
daily_df = (
    df_model.groupby('Date')['Transaction_amount']
    .sum()
    .reset_index()
    .rename(columns={'Transaction_amount': 'Daily_Spend'})
)

