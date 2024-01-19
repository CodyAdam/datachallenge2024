import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


# open xlsx
file_path = './data/federalfinancegestion/clean_dataset.pkl'
data = pd.read_pickle(file_path)

# remove date column
data = data.drop('date', axis=1)
data = data.drop('id', axis=1)

# Preprocessing
# Removing columns with a high number of missing values
threshold = 0.2 * len(data)  # 20% of the total number of rows
columns_to_drop = data.columns[data.isnull().sum() > threshold]
data_cleaned = data.drop(columns=columns_to_drop)

# Filling remaining missing values with the median of each column
data_cleaned = data_cleaned.fillna(data_cleaned.median())

# Dropping non-numeric columns
non_numeric_columns = data_cleaned.select_dtypes(include=['object', 'datetime']).columns
data_cleaned = data_cleaned.drop(non_numeric_columns, axis=1)

# Preparing the data for Random Forest
X = data_cleaned.drop('Close_BTC', axis=1)
y = data_cleaned['Close_BTC']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Training the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Getting the feature importances
feature_importances = rf_model.feature_importances_

# Creating a DataFrame to view feature importances
features_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

# Displaying the top 10 features for clarity
print(features_df.head(10))

write_path = './data/federalfinancegestion/close_btc_rf_importance.xlsx'
features_df.to_excel(write_path)

