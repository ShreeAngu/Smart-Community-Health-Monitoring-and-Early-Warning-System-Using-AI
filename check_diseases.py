import pandas as pd

df = pd.read_csv('Data/water_disease_data.csv')

print("=" * 0)
print("DISEASES IN YOUR DATASET")
print("=" * 0)

print("\nDisease distribution:")
print(df['disease'].value_counts())

print(f"\nTotal unique diseases: {df['disease'].nunique()}")
print("\nUnique disease names:")
for disease in sorted(df['disease'].unique()):
 print(f" - {disease}")
