"""
Test script for column mapping utility

Run with: python backend/test_column_mapping.py
"""

from utils.column_mapping import get_friendly_name, get_technical_name, get_all_mappings

def test_column_mapping():
 """Test the column mapping utility"""

 print("=" * 0)
 print(" TESTING COLUMN MAPPING UTILITY")
 print("=" * 0)

 # Test cases
 test_cases = [
 "fecal_coliform_per_00ml",
 "ph",
 "turbidity_ntu",
 "arsenic_ug_l",
 "symptom_diarrhea",
 "water_quality_index",
 "avg_rainfall_mm",
 "unknown_column" # Test fallback
 ]

 print("\n Testing get_friendly_name():")
 print("-" * 0)
 for column in test_cases:
 friendly = get_friendly_name(column)
 print(f" {column:0s} → {friendly}")

 print("\n Testing reverse lookup (get_technical_name()):")
 print("-" * 0)
 friendly_names = [
 "Fecal Bacteria Count",
 "Water pH Level",
 "Arsenic Level"
 ]
 for friendly in friendly_names:
 technical = get_technical_name(friendly)
 print(f" {friendly:0s} → {technical}")

 print("\n Total mappings available:")
 print("-" * 0)
 mappings = get_all_mappings()
 print(f" {len(mappings)} column mappings defined")

 # Group by category
 categories = {
 "Water Quality": ["ph", "turbidity_ntu", "fecal_coliform_per_00ml", "arsenic_ug_l"],
 "Symptoms": ["symptom_diarrhea", "symptom_fever", "symptom_vomiting"],
 "Environmental": ["avg_temperature_c", "avg_rainfall_mm", "flooding"],
 "Demographics": ["age", "gender", "region", "district"]
 }

 print("\n Mappings by Category:")
 print("-" * 0)
 for category, columns in categories.items():
 print(f"\n {category}:")
 for col in columns:
 if col in mappings:
 print(f" • {col:0s} → {mappings[col]}")

 print("\n" + "=" * 0)
 print(" Column mapping utility test complete!")
 print("=" * 0)

if __name__ == "__main__":
 test_column_mapping()
