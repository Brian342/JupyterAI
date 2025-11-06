import matplotlib.pyplot as plt
from prophet import Prophet
import pandas as pd

df_model = pd.read_csv("statement_cleaned")


def create_net_flow(df):
    # normalize the text to lowercase for easy matching
    df['flow_type'] = df['paid_in_or_Withdraw'].str.lower()

    # map incoming/outgoing transactions
    def classify_flow(flow):
        if any(x in flow for x in ['paid in', 'deposit', 'received']):
            return 1  # money coming in
        elif any(x in flow for x in ['withdraw', 'sent', 'buy goods', 'payment', 'airtime']):
            return -1  # money going out
        else:
            return 0  # neutral / unknown

    df['flow_direction'] = df['flow_type'].apply(classify_flow)

    # create net flow column
    df['Net_Flow'] = df['Transaction_amount'] * df['flow_direction']

    return df


# example usage
df_model = create_net_flow(df_model)

# check results
print(df_model[['Date', 'Transaction_amount', 'paid_in_or_Withdraw', 'Net_Flow']].head())
