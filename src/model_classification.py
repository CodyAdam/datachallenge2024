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
file_path = '../data/federalfinancegestion/clean_dataset.pkl'  # Replace with your file path
crypto_data = pd.read_pickle(file_path)

# Fill missing values
crypto_data.fillna(0, inplace=True)

# Create target variable (ensure no NaN values)
crypto_data['Target'] = np.sign(crypto_data['Close_BTC'].diff().shift(-1))
crypto_data.dropna(subset=['Target'], inplace=True)  # Drop any rows with NaN in 'Target'

# Select features and target
filtered_columns = [col for col in crypto_data.columns if not any(black_word in col.lower() for black_word in blacklist)]
# print(len(crypto_data.columns), len(filtered_columns))
# print(filtered_columns)
# exit()
features = crypto_data[filtered_columns].select_dtypes(include=['float64', 'int64']).drop(['Close_BTC'], axis=1)
target = crypto_data['Target']

# Split the data (replace the dates with your specific dates)
train_data = crypto_data[crypto_data['date'] < '2022-08-01']
test_data = crypto_data[crypto_data['date'] >= '2022-08-01']

# Split features and target
X_train = train_data[features.columns]
y_train = train_data['Target']
X_test = test_data[features.columns]
y_test = test_data['Target']

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Reshape input for LSTM
X_train_reshaped = X_train_scaled.reshape((X_train_scaled.shape[0], 1, X_train_scaled.shape[1]))
X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], 1, X_test_scaled.shape[1]))

# Build LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(1, X_train_reshaped.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(1, activation='tanh'))  # Output range [-1, 1]

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

# Train the model
model.fit(X_train_reshaped, y_train, epochs=50, batch_size=16, verbose=1)

# Predict and evaluate
y_pred = model.predict(X_test_reshaped).flatten()
y_pred_class = np.sign(y_pred)
y_pred_class = np.where(np.isnan(y_pred_class), 0, y_pred_class)  # Replace NaN predictions with 0

accuracy = accuracy_score(y_test, y_pred_class)
precision = precision_score(y_test, y_pred_class, average='macro')
recall = recall_score(y_test, y_pred_class, average='macro')
f1 = f1_score(y_test, y_pred_class, average='macro')

test_data['pred_direction'] = y_pred_class
test_data['close_direction'] = np.sign(test_data['Close_BTC'].diff().shift(-1))
test_data['pred_correct'] = np.where(test_data['close_direction'] * test_data['pred_direction'] > 0, 1, -1)
test_data['money'] =  abs(test_data['Close_BTC'].shift(-1) - test_data['Close_BTC']) * test_data['pred_correct']
test_data['money_acc'] = test_data['money'].cumsum()

print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1 Score: {f1}')

# Visualization of results
plt.figure(figsize=(12, 10))

# Bitcoin Price Plot
plt.subplot(3, 1, 1)
plt.plot(test_data['date'], test_data['Close_BTC'], label='Actual BTC Price')
plt.title('Bitcoin Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Price Change Plot
plt.subplot(3, 1, 2)
plt.plot(test_data['date'], y_test, label='Actual Change')
plt.plot(test_data['date'], y_pred_class, label='Predicted Change', alpha=0.7)
plt.title('Actual vs Predicted Price Change')
plt.xlabel('Date')
plt.ylabel('Change')
plt.legend()

# Money Plot
plt.subplot(3, 1, 3)
plt.plot(test_data['date'], test_data['money_acc'], label='Money Accumulated')
plt.title('Money Accumulated Over Time')
plt.xlabel('Date')
plt.ylabel('Money ($)')
plt.legend()


plt.tight_layout()
plt.show()
