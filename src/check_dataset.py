import pandas as pd

df = pd.read_csv("data/processed/lol_ranked_dataset.csv")

print("SHAPE:")
print(df.shape)

print("\nCOLUMNS:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head())

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nDUPLICATES:")
print(df.duplicated().sum())