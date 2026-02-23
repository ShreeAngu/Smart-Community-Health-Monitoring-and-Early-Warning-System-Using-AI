import pandas as pd
import numpy as np

# Load the dataset
data_path = 'Data/water_disease_data.csv'
df = pd.read_csv(data_path)

print("=" * 0)
print("DATASET EXPLORATION")
print("=" * 0)

# Print shape
print(f"\nDataset Shape: {df.shape}")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[]}")

# Print columns
print("\n" + "=" * 0)
print("COLUMNS IN DATASET")
print("=" * 0)
print(df.columns.tolist())

# Expected columns
expected_columns = [
 'region', 'latitude', 'longitude', 'is_urban', 'population_density',
 'age', 'gender', 'water_source', 'water_treatment', 'water_quality_index',
 'ph', 'turbidity_ntu', 'dissolved_oxygen_mg_l', 'bod_mg_l',
 'fecal_coliform_per_00ml', 'total_coliform_per_00ml', 'tds_mg_l',
 'nitrate_mg_l', 'fluoride_mg_l', 'arsenic_ug_l', 'open_defecation_rate',
 'toilet_access', 'sewage_treatment_pct', 'handwashing_practice',
 'month', 'season', 'avg_temperature_c', 'avg_rainfall_mm',
 'avg_humidity_pct', 'flooding', 'symptom_diarrhea', 'symptom_vomiting',
 'symptom_fever', 'symptom_abdominal_pain', 'symptom_dehydration',
 'symptom_jaundice', 'symptom_bloody_stool', 'symptom_skin_rash', 'disease'
]

print(f"\nExpected columns: {len(expected_columns)}")
print(f"Actual columns: {len(df.columns)}")

# Check for missing or extra columns
missing_cols = set(expected_columns) - set(df.columns)
extra_cols = set(df.columns) - set(expected_columns)

if missing_cols:
 print(f"\nMissing columns: {missing_cols}")
if extra_cols:
 print(f"\nExtra columns: {extra_cols}")
if not missing_cols and not extra_cols:
 print("\n All expected columns are present!")

# Check for null values
print("\n" + "=" * 0)
print("NULL VALUES CHECK")
print("=" * 0)
null_counts = df.isnull().sum()
null_percentages = (df.isnull().sum() / len(df)) * 00

null_summary = pd.DataFrame({
 'Column': null_counts.index,
 'Null Count': null_counts.values,
 'Null Percentage': null_percentages.values
})

null_summary = null_summary[null_summary['Null Count'] > 0].sort_values('Null Count', ascending=False)

if len(null_summary) > 0:
 print("\nColumns with missing values:")
 print(null_summary.to_string(index=False))
else:
 print("\n No missing values found!")

# Data types
print("\n" + "=" * 0)
print("DATA TYPES")
print("=" * 0)
print(df.dtypes)

# Basic statistics for target variable
print("\n" + "=" * 0)
print("TARGET VARIABLE (disease) DISTRIBUTION")
print("=" * 0)
if 'disease' in df.columns:
 print(df['disease'].value_counts())
 print(f"\nTotal unique diseases: {df['disease'].nunique()}")

print("\n" + "=" * 0)
print("FIRST FEW ROWS")
print("=" * 0)
print(df.head())

print("\n" + "=" * 0)
print("SUMMARY STATISTICS")
print("=" * 0)
print(df.describe())
