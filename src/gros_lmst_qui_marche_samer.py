import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Dense, Input
import matplotlib.pyplot as plt

# Load data
dataset_pickle = './data/federalfinancegestion/dataset.pkl'
df = pd.read_pickle(dataset_pickle)
df.fillna(0, inplace=True)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

start_date_training = pd.to_datetime('2017-08-01')
end_date_training = pd.to_datetime('2022-08-31')
start_date_testing = pd.to_datetime('2022-09-01')
end_date_testing = pd.to_datetime('2023-04-30')

train_df = df.loc[start_date_training:end_date_training]
test_df = df.loc[start_date_testing:end_date_testing]

# Include 'Volume_BTC' and 'crisis_textblob_polarity_mean' as additional features
btc_train = train_df[['Close_BTC', 'Volume_BTC', 'crisis_textblob_polarity_mean']].values
btc_test = test_df[['Close_BTC', 'Volume_BTC', 'crisis_textblob_polarity_mean']].values

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
btc_train_scaled = scaler.fit_transform(btc_train)
btc_test_scaled = scaler.transform(btc_test)

# # # SDAE
# input_layer = Input(shape=(3,))
# encoded = Dense(64, activation='relu')(input_layer)
# encoded = Dense(32, activation='relu')(encoded)
# encoded = Dense(16, activation='relu')(encoded)

# decoded = Dense(32, activation='relu')(encoded)
# decoded = Dense(64, activation='relu')(decoded)
# decoded = Dense(3, activation='sigmoid')(decoded)

# autoencoder = Model(input_layer, decoded)
# autoencoder.compile(optimizer='adam', loss='mse')

# # Train the autoencoder
# autoencoder.fit(btc_train_scaled, btc_train_scaled, epochs=150, batch_size=32, shuffle=True, validation_split=0.2)

# # Get the encoded representation of the data
# encoded_features = autoencoder.predict(btc_train_scaled)

def create_sequences(data, sequence_length):
    xs, ys = [], []
    for i in range(len(data) - sequence_length):
        x = data[i:(i + sequence_length), :]
        y = data[i + sequence_length, 0]  # The target is still 'Close_BTC' price
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

sequence_length = 10  # Number of days used to predict the next day
X_train, y_train = create_sequences(btc_train_scaled, sequence_length)
X_test, y_test = create_sequences(btc_test_scaled, sequence_length)

# # Reshape inputs for LSTM [samples, time steps, features]
# X_train, y_train = create_sequences(encoded_features, sequence_length)

# Reshape inputs for LSTM [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 3)) # 3 features now
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 3))

# Build the LSTM model
model = Sequential()
model.add(LSTM(100, return_sequences=True, input_shape=(sequence_length, 3))) # Adjusted for 3 features
model.add(LSTM(100, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, batch_size=64, epochs=100)

predictions = model.predict(X_test)
# Reshape predictions to match the scaler's expected input for inverse transformation
predictions = scaler.inverse_transform(np.concatenate((predictions, np.zeros((predictions.shape[0], 2))), axis=1))[:, 0]

# Slice the actual prices to align with the predictions
actual_prices_aligned = df.loc[start_date_testing:end_date_testing, 'Close_BTC'][-len(predictions):].reset_index(drop=True)

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

# Plotting
plt.figure(figsize=(16, 8))
plt.plot(actual_prices_aligned, label='Actual Price', color='blue')
plt.plot(predictions, label='Predicted Price', color='red', alpha=0.7)
plt.title('Bitcoin Price Prediction')
plt.xlabel('Time')
plt.ylabel('BTC Price')
plt.legend()
plt.show()
