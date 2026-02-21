"""
Test script for column mapping utility

Run with: python backend/test_column_mapping.py
"""

from utils.column_mapping import get_friendly_name, get_technical_name, get_all_mappings

def test_column_mapping():
    """Test the column mapping utility"""
    
    print("=" * 80)
    print("🧪 TESTING COLUMN MAPPING UTILITY")
    print("=" * 80)
    
    # Test cases
    test_cases = [
        "fecal_coliform_per_100ml",
        "ph",
        "turbidity_ntu",
        "arsenic_ug_l",
        "symptom_diarrhea",
        "water_quality_index",
        "avg_rainfall_mm",
        "unknown_column"  # Test fallback
    ]
    
    print("\n📋 Testing get_friendly_name():")
    print("-" * 80)
    for column in test_cases:
        friendly = get_friendly_name(column)
        print(f"  {column:30s} → {friendly}")
    
    print("\n🔄 Testing reverse lookup (get_technical_name()):")
    print("-" * 80)
    friendly_names = [
        "Fecal Bacteria Count",
        "Water pH Level",
        "Arsenic Level"
    ]
    for friendly in friendly_names:
        technical = get_technical_name(friendly)
        print(f"  {friendly:30s} → {technical}")
    
    print("\n📊 Total mappings available:")
    print("-" * 80)
    mappings = get_all_mappings()
    print(f"  {len(mappings)} column mappings defined")
    
    # Group by category
    categories = {
        "Water Quality": ["ph", "turbidity_ntu", "fecal_coliform_per_100ml", "arsenic_ug_l"],
        "Symptoms": ["symptom_diarrhea", "symptom_fever", "symptom_vomiting"],
        "Environmental": ["avg_temperature_c", "avg_rainfall_mm", "flooding"],
        "Demographics": ["age", "gender", "region", "district"]
    }
    
    print("\n📂 Mappings by Category:")
    print("-" * 80)
    for category, columns in categories.items():
        print(f"\n  {category}:")
        for col in columns:
            if col in mappings:
                print(f"    • {col:30s} → {mappings[col]}")
    
    print("\n" + "=" * 80)
    print("✅ Column mapping utility test complete!")
    print("=" * 80)


if __name__ == "__main__":
    test_column_mapping()
