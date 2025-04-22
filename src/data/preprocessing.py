import pandas as pd

data = pd.read_csv('data/processed/cleaned_data.csv')
data = data.drop_duplicates()
data = data.dropna(axis = 1, how = 'all')
data = data.dropna(subset=['price'])
for col in ['owners', 'seats']:
    if col in data.columns:
        mode = data[col].mode()[0]
        data[col] = data[col].fillna(mode)
