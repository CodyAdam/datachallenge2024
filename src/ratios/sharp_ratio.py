import numpy as np
import pandas as pd


dataset_pickle = './data/federalfinancegestion/dataset.pkl'
df = pd.read_pickle(dataset_pickle)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df.fillna(0, inplace=True)

TRADING_DAYS_PER_YEAR = 365

start_date_training = pd.to_datetime('2017-08-01')
end_date_training = pd.to_datetime('2022-08-31')
start_date_testing = pd.to_datetime('2022-09-01')
end_date_testing = pd.to_datetime('2023-04-30')

train_df = df.loc[start_date_training:end_date_training]
test_df = df.loc[start_date_testing:end_date_testing].copy()

test_df['daily_returns'] = test_df['Close_BTC'].pct_change(1)
risk_free_rate = 0.01 / TRADING_DAYS_PER_YEAR
excess_returns = test_df['daily_returns'] - risk_free_rate
sharpe_ratio = excess_returns.mean() / excess_returns.std()
sharpe_ratio_annualized = sharpe_ratio * np.sqrt(TRADING_DAYS_PER_YEAR)

print(round(sharpe_ratio_annualized, 3))