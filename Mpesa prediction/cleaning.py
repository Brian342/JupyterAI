# code cleaning area
from dateutil import parser


def remove_comma(x):
    """This function removes commas on the dataset
    parameters: x,
    return x"""
    x = str(x)
    x = x.replace(',', '')
    return x


# Anonymising the dataset
def transaction(x):
    x = str(x).strip()
    if x.startswith('Merchant Payment'):
        index = x.find(' - ') + 2
        name = x[index:].strip().upper()

        return 'BUY GOODS', name

    elif x.startswith('Deposit of funds'):
        index = x.find(' - ')
        name = x[index:].strip().upper()

        return 'AGENT DEPOSIT', name

    elif x.startswith('OD Loan Repayment'):
        return 'FULIZA REPAYMENT', 'FULIZA'

    elif x.startswith('OverDraft of Credit Party'):
        return 'FULIZA TAKEN', 'FULiZA'

    elif x.startswith('M-Shwari Deposit'):
        return 'M-SHWARI DEPOSIT FROM M-PESA', 'M-SHWARI'

    elif x.startswith('KCB M-PESA Deposit'):
        return 'KCB M-PESA DEPOSIT FROM M-PESA', 'KCB DEPOSIT'

    elif x.startswith('KCB M-PESA Withdraw'):
        return 'KCB M-PESA WITHDRAW FROM M-PESA', 'KCB WITHDRAW'

    elif x.startswith('Customer Transfer'):
        index = x.find(' - ')
        to_search = x[index:]
        last = 1

        for i in range(len(to_search)):
            try:
                int(to_search[i])
                last = i

            except:
                v = 10

        name = x[index + last + 2:].strip().upper()
        return 'SEND MONEY', name

    elif x.startswith('M-Shwari Withdraw'):

        return 'M-SHWARI WITHDRAW FROM M-PESA', 'M-SHWARI WITHDRAW'

    elif x.startswith('Pay Bill'):
        if x.strip() == 'Pay Bill Charge':

            return 'PAY BILL CHARGES', 'TRANSACTION COST'
        else:
            index = x.find(' - ') + 2
            end = x.lower().find('acc')
            name = x[index:end].strip().upper()

            return 'PAY BILL', name

    elif x.startswith('Funds received'):
        index = x.find(' - ')
        to_search = x[index:]
        last = 1

        for i in range(len(to_search)):
            try:
                int(to_search[i])
                last = i
            except:
                v = 10

        name = x[index + last + 2:].strip().upper()

        return 'RECEIVED FUNDS', name

    elif x.startswith('Customer Payment to Small Business') or x.startswith('Customer Send Money'):
        index = x.find(' - ')
        to_search = x[index:]
        last = 1

        for i in range(len(to_search)):
            try:
                int(to_search[i])
                last = i
            except:
                v = 10

        name = x[index + last + 2:].strip().upper()

        return 'POCHI LA BIASHARA', name

    elif x.startswith('Airtime Purchase'):
        return 'AIRTIME PURCHASE', 'AIRTIME'

    elif x.startswith('Business Payment From'):
        index = x.find(' - ')
        end = x.lower().find('via')
        to_search = x[index:]
        last = 1
        name = x[index:end].strip().upper()
        return 'FUNDS RECEIVED FROM BUSINESS', name

    elif x.startswith('Customer Transfer of Funds Charge'):
        return 'TRANSACTION COST', 'TRANSACTION COST'

    elif x.startswith('Buy Bundles Online'):
        return 'BUNDLES PURCHASE', 'BUNDES PURCHASE'

    elif x.startswith('Customer Withdrawal'):
        index = x.find(' - ')
        name = x[index:].strip().upper()
        return 'CASH WITHDRAWAL', name

    elif x.startswith('Withdrawal Charge'):
        return 'CASH WITHDRAWAL CHARGES', "TRANSACTION COST"

    elif x.startswith('Savings Contribution'):
        return 'TO HUSTLER FUND SAVINGS', 'HUSTLER FUND'

    elif x.startswith('Term Loan Disbursement for H- Fund') or x.startswith('Term Loan Disbursement for H-Fund'):
        return 'HUSTLER FUND Disbursement'.upper(), 'HUSTLER FUND'

    elif x.startswith('Term Loan Repayment for H- Fund') or x.startswith('Term Loan Repayment for H-Fund'):
        return 'HUSTLER FUND REPAYMENT', 'HUSTLER FUND'

    else:
        return 'UNIDENTIFIED', 'UNIDENTIFIED'


def change_date(date):
    date = parser.parse(date)
    return date.year, date.month, date.day, date.weekday(), date.hour, date.minute, date.second


def withdrawAmount(x):
    try:
        if x < 0:
            return -x
        else:
            return x
    except:
        return x

