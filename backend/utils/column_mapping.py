"""
Column Mapping Utility

This module provides a mapping from technical database column names
to human-readable display names for the frontend.

Usage:
    from backend.utils.column_mapping import get_friendly_name
    
    friendly = get_friendly_name("fecal_coliform_per_100ml")
    # Returns: "Fecal Bacteria Count"
"""

# Comprehensive mapping of technical column names to user-friendly names
COLUMN_MAPPING = {
    # Location & Demographics
    "district": "District",
    "region": "Region",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "is_urban": "Urban/Rural Area",
    "population_density": "Population Density",
    "age": "Patient Age",
    "gender": "Patient Gender",
    
    # Water Source & Treatment
    "water_source": "Primary Water Source",
    "water_treatment": "Water Treatment Method",
    "water_quality_index": "Water Quality Score (WQI)",
    
    # Water Quality Parameters
    "ph": "Water pH Level",
    "turbidity_ntu": "Water Cloudiness (Turbidity)",
    "dissolved_oxygen_mg_l": "Dissolved Oxygen Level",
    "bod_mg_l": "Biological Oxygen Demand (BOD)",
    "fecal_coliform_per_100ml": "Fecal Bacteria Count",
    "total_coliform_per_100ml": "Total Bacteria Count",
    "tds_mg_l": "Total Dissolved Solids (TDS)",
    "nitrate_mg_l": "Nitrate Level",
    "fluoride_mg_l": "Fluoride Level",
    "arsenic_ug_l": "Arsenic Level",
    
    # Sanitation & Hygiene
    "open_defecation_rate": "Local Open Defecation Rate",
    "toilet_access": "Access to Toilets",
    "sewage_treatment_pct": "Sewage Treatment Coverage",
    "handwashing_practice": "Handwashing Hygiene Level",
    
    # Environmental & Temporal
    "month": "Month of Report",
    "season": "Season",
    "avg_temperature_c": "Average Temperature (°C)",
    "avg_rainfall_mm": "Average Rainfall (mm)",
    "avg_humidity_pct": "Average Humidity (%)",
    "flooding": "Recent Flooding Event",
    
    # Symptoms
    "symptom_diarrhea": "Symptom: Diarrhea",
    "symptom_vomiting": "Symptom: Vomiting",
    "symptom_fever": "Symptom: Fever",
    "symptom_abdominal_pain": "Symptom: Abdominal Pain",
    "symptom_dehydration": "Symptom: Dehydration",
    "symptom_jaundice": "Symptom: Jaundice",
    "symptom_bloody_stool": "Symptom: Bloody Stool",
    "symptom_skin_rash": "Symptom: Skin Rash",
    
    # Disease
    "disease": "Diagnosed Disease"
}


def get_friendly_name(column_name: str) -> str:
    """
    Convert a technical column name to a human-readable display name.
    
    Args:
        column_name: The technical column name (e.g., "fecal_coliform_per_100ml")
    
    Returns:
        Human-readable name (e.g., "Fecal Bacteria Count")
        If no mapping exists, returns a title-cased version with underscores replaced
    
    Examples:
        >>> get_friendly_name("fecal_coliform_per_100ml")
        'Fecal Bacteria Count'
        
        >>> get_friendly_name("ph")
        'Water pH Level'
        
        >>> get_friendly_name("unknown_column")
        'Unknown Column'
    """
    return COLUMN_MAPPING.get(column_name, column_name.replace('_', ' ').title())


def get_all_mappings() -> dict:
    """
    Get the complete column mapping dictionary.
    
    Returns:
        Dictionary of all column name mappings
    """
    return COLUMN_MAPPING.copy()


def get_technical_name(friendly_name: str) -> str:
    """
    Reverse lookup: Convert a friendly name back to technical column name.
    
    Args:
        friendly_name: The human-readable name
    
    Returns:
        Technical column name, or the input if no match found
    
    Examples:
        >>> get_technical_name("Fecal Bacteria Count")
        'fecal_coliform_per_100ml'
    """
    # Create reverse mapping
    reverse_mapping = {v: k for k, v in COLUMN_MAPPING.items()}
    return reverse_mapping.get(friendly_name, friendly_name)


# Export commonly used functions
__all__ = ['get_friendly_name', 'get_all_mappings', 'get_technical_name', 'COLUMN_MAPPING']
