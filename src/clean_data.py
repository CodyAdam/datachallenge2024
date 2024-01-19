import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

# Load the dataset
file_path = './data/federalfinancegestion/Rennes_DataChallenge2024_Cryptomarkets_dataset.xlsx'
data = pd.read_excel(file_path)

# rename first column to "id"
data.rename(columns={data.columns[0]: "id"}, inplace=True)

# Replace "." with numpy NaN
data.replace(".", np.nan, inplace=True)

TO_IMPUTE = ['SP500',
             'NASDAQComposite',
             '13WeeksTreasuryBill',
             'TreasuryYield5Years',
             'TreasuryYield10Years',
             'TreasuryYield30Years',
             'H15T1M_Index',
             'H15T3M_Index',
             'H15T6M_Index',
             'H15T1Y_Index',
             'H15T2Y_Index',
             'H15T5Y_Index',
             'H15T3Y_Index',
             'H15T10Y_Index',
             'InflationBreakevenT5YIE',
             'InflationBreakevenT10YIE',
             'VIXCLS',
             'VXNCLS',
             'VXVCLS',
             'US0001M_Index',
             'US0003M_Index',
             'US0006M_Index',
             'US0012M_Index',
             'WTI_CrudeOil',
             'CDS_ITRXEUE',
             'CDS_ITRXEXE',
             'CDS_ITRXEBE',
             'CDS_ITRXESE',
             'USEPUINDXD',
             ]


# Select and convert the columns to impute to numeric
data_to_impute = data[TO_IMPUTE].apply(pd.to_numeric, errors='coerce')

# Initialize the KNN Imputer
imputer = KNNImputer(n_neighbors=5, weights='uniform')

# Perform the imputation
imputed_data = imputer.fit_transform(data_to_impute)

# Convert the result back to a DataFrame
imputed_data = pd.DataFrame(imputed_data, columns=data_to_impute.columns)

# Replace the original data columns with the imputed data
data[TO_IMPUTE] = imputed_data

# Save the imputed data to a new file (optional)
output_path = './data/federalfinancegestion/clean_dataset.pkl'
data.to_pickle(output_path)

output_path = './data/federalfinancegestion/clean_dataset.xlsx'
data.to_excel(output_path)


print("Data imputed and saved to {}".format(output_path))
