
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# open xlsx
file_path = './data/federalfinancegestion/Rennes_DataChallenge2024_Cryptomarkets_dataset.xlsx'
data = pd.read_excel(file_path)

# Remove all string (object type) columns from the dataset
data_numeric = data.select_dtypes(exclude=['object'])

# Finding the column that closely matches "Close_BTC" in the numeric dataset
close_btc_column_numeric = [col for col in data_numeric.columns if "Close_BTC" in col]

# Check if there is exactly one match for "Close_BTC"
if len(close_btc_column_numeric) == 1:
    close_btc_column_numeric = close_btc_column_numeric[0]
    # Calculate the correlation of all columns with Close_BTC in the numeric dataset
    correlation_with_close_btc_numeric = data_numeric.corr()[close_btc_column_numeric].sort_values(ascending=False)
else:
    correlation_with_close_btc_numeric = "Unable to find a unique column matching 'Close_BTC'."

print(correlation_with_close_btc_numeric)

# output to xlsx
output_path = './data/federalfinancegestion/close_btc_correlation.xlsx'
correlation_with_close_btc_numeric.to_excel(output_path)
