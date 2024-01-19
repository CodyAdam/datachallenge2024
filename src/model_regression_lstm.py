import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from lists import whitelist, blacklist

# Load your dataset
file_path = './data/federalfinancegestion/clean_dataset.pkl'  # Replace with your file path
data = pd.read_pickle(file_path)

CUR = "Close_BTC"

data.fillna(0, inplace=True)

# Create target variable (ensure no NaN values)
data['TomorowClose'] = data[CUR].shift(-1)

# Select features and target
filtered_columns = [col for col in data.columns if not any(black_word in col.lower() for black_word in blacklist)]

features = data[filtered_columns].select_dtypes(include=['float64', 'int64']).drop([CUR, 'TomorowClose'], axis=1)

# Split the data (replace the dates with your specific dates)
train_data = data[data['date'] < '2022-08-01']
test_data = data[data['date'] >= '2022-08-01']

# Split features and target
X_train = train_data[features.columns]
y_train = train_data['TomorowClose']
X_test = test_data[features.columns]
y_test = test_data['TomorowClose']

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Reshape input for LSTM
X_train_reshaped = X_train_scaled.reshape((X_train_scaled.shape[0], 1, X_train_scaled.shape[1]))
X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], 1, X_test_scaled.shape[1]))

# Build LSTM model
model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(1, X_train_reshaped.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(1, activation='linear'))
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
model.fit(X_train_reshaped, y_train, epochs=250, batch_size=16, verbose=1)

y_pred = model.predict(X_test_reshaped).flatten()

INITIAL_MONEY = 1000
money = INITIAL_MONEY
alpha = 0.5
# calculate money over time (when betting alpha * money) if prediction correct gain alpha * money * percent_diff else lose alpha * money * percent_diff
test_data['money_acc'] = 0
for i in range(len(y_pred) - 1):
    percent_diff = (y_test.iloc[i + 1] - y_test.iloc[i]) / y_test.iloc[i]
    prediction_correct = (y_pred[i] > y_test.iloc[i]) == (y_test.iloc[i + 1] > y_test.iloc[i])

    if prediction_correct:
        money += alpha * money * abs(percent_diff)
    else:
        money -= alpha * money * abs(percent_diff)

    test_data['money_acc'].iloc[i] = money
test_data['money_acc'].iloc[-1] = money

# Visualization of results
plt.figure(figsize=(12, 10))

# Bitcoin Price Plot
plt.subplot(3, 1, 1)
plt.plot(test_data['date'], test_data[CUR], label='Actual Price')
plt.title('Bitcoin Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Price Change Plot
plt.subplot(3, 1, 2)
plt.plot(test_data['date'], y_test, label='Actual Change')
plt.plot(test_data['date'], y_pred, label='Predicted Change', alpha=0.7)
plt.title('Actual vs Predicted Price Change')
plt.xlabel('Date')
plt.ylabel('Change')
plt.legend()

# Money Accumulated Plot
plt.subplot(3, 1, 3)
plt.plot(test_data['date'], test_data['money_acc'], label='Money Accumulated')
plt.title('Money Accumulated Over Time')
plt.xlabel('Date')
plt.ylabel('Money ($)')
plt.axhline(INITIAL_MONEY, color='red', linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.show()
