import pandas as pd
import time
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import numpy as np

### Load data
DATA_PATH = 'data/federalfinancegestion/dataset.pkl'
df = pd.read_pickle(DATA_PATH)

# Preprocess the df
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Replace 'Close_BTC' with the column for the cryptocurrency you're interested in
crypto_column = 'Close_BTC'
X = df[crypto_column].values.reshape(-1, 1)

# Splitting the df
split_date = '2022-08-31'
X_train = X[df.index <= split_date]
X_test = X[df.index > split_date]

# Normalizing the df
scaler = MinMaxScaler(feature_range=(0, 1))
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Creating dfset for LSTM
def create_dfset(X, time_steps=1):
    Xs = []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:(i + time_steps), 0])
    return np.array(Xs)

time_steps = 1
X_train_final = create_dfset(X_train_scaled, time_steps)
X_test_final = create_dfset(X_test_scaled, time_steps)

# Reshape input to be [samples, time steps, features]
X_train_final = X_train_final.reshape(X_train_final.shape[0], X_train_final.shape[1], 1)
X_test_final = X_test_final.reshape(X_test_final.shape[0], X_test_final.shape[1], 1)

# Define the LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train_final.shape[1], 1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=25))
model.add(Dense(units=1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train_final, X_train_final, epochs=1, batch_size=1)  # Increase epochs for better performance

# Predict and evaluate
predicted = model.predict(X_test_final)
predicted_prices = scaler.inverse_transform(predicted.reshape(-1, 1))

for i in range(len(predicted_prices)):
    predicted = predicted_prices[i][0]
    actual = X_test[i + 1][0]
    diff = predicted - actual
    abs_diff = abs(diff)
    print(f"{predicted:.2f}\t{actual:.2f}\t{diff:.2f}\t{abs_diff:.2f}")