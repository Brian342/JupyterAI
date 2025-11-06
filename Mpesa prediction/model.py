import pandas as pd
df_model = pd.read_csv("statement_cleaned")
df_model['Date'] = pd.to_datetime(df_model['Date'], errors='coerce')

# keeping only outgoing (spending) transactions
df_model = df_model[df_model['paid_in_or_Withdraw'].str.contains('Withdraw', case=False, na=False)]

# handling missing values
df_model = df_model.dropna(subset=['Transaction_amount', 'Date'])
df_model = df_model[df_model['Transaction_amount'] >0 ]
