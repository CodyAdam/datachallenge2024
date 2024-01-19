import pandas as pd
import time

START_TIME = time.time()
DATA_PATH = 'data/federalfinancegestion/dataset.pkl'


df = pd.read_pickle(DATA_PATH)
print(f"[*] Loaded in {time.time() - START_TIME}")
print(df.head())
