import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import math
from lists import whitelist, blacklist
# Load your dataset
file_path = '../data/federalfinancegestion/clean_dataset.pkl'  # Replace with your file path
crypto_data = pd.read_pickle(file_path)

# Forward fill and backfill to handle NaNs
crypto_data.ffill(inplace=True)
crypto_data.bfill(inplace=True)

# Create target variable (next day's Close_BTC)
crypto_data['Target'] = crypto_data['Close_BTC'].shift(-1)
crypto_data.dropna(subset=['Target'], inplace=True)

# Selecting features and target while excluding blacklisted columns
filtered_columns = [col for col in crypto_data.columns if not any(black_word in col.lower() for black_word in blacklist)] # Blacklist
filtered_columns = [col for col in crypto_data.columns if col in whitelist]  # Whitelist
features = crypto_data[filtered_columns].select_dtypes(include=['float64', 'int64']).drop(['Close_BTC'], axis=1)
target = crypto_data['Target']

# Split the data
train_data = crypto_data[crypto_data['date'] < '2022-08-01']
test_data = crypto_data[crypto_data['date'] >= '2022-08-01']

# Split features and target
X_train = train_data[features.columns]
y_train = train_data['Target']
X_test = test_data[features.columns]
y_test = test_data['Target']

# Normalize features
feature_scaler = StandardScaler()
X_train_scaled = feature_scaler.fit_transform(X_train)
X_test_scaled = feature_scaler.transform(X_test)

# Scale target variable
target_scaler = StandardScaler()
y_train_scaled = target_scaler.fit_transform(y_train.values.reshape(-1, 1))

# Reshape input for LSTM
X_train_reshaped = X_train_scaled.reshape((X_train_scaled.shape[0], 1, X_train_scaled.shape[1]))
X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], 1, X_test_scaled.shape[1]))

# Build LSTM model for regression
model = Sequential()
model.add(LSTM(50, activation='tanh', input_shape=(1, X_train_reshaped.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(1))

# Compile the model with gradient clipping
opt = Adam(learning_rate=0.001, clipvalue=1.0)
model.compile(optimizer=opt, loss='mean_squared_error')

# Train the model
model.fit(X_train_reshaped, y_train_scaled, epochs=100, batch_size=16, verbose=1)

# Predict and evaluate
y_pred_scaled = model.predict(X_test_reshaped).flatten()
y_pred = target_scaler.inverse_transform(y_pred_scaled.reshape(-1, 1))

# Regression metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = math.sqrt(mean_squared_error(y_test, y_pred))

print(f'Mean Absolute Error: {mae}')
print(f'Root Mean Squared Error: {rmse}')

# Visualization of results
plt.figure(figsize=(12, 6))
plt.plot(test_data['date'], y_test, label='Actual BTC Price')
plt.plot(test_data['date'], y_pred, label='Predicted BTC Price', alpha=0.7)
plt.title('Actual vs Predicted BTC Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
