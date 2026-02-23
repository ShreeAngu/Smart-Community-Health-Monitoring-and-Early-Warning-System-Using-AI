"""
CSV Sync Utility
Appends new report data to the training CSV file for continuous learning
"""
import pandas as pd
import os
from datetime import datetime
from typing import Dict, Any
import json

def append_report_to_csv(report_data: Dict[str, Any], prediction_data: Dict[str, Any]) -> bool:
 """
 Append a new report to the water_disease_data.csv file

 Args:
 report_data: Dictionary containing report information
 prediction_data: Dictionary containing prediction results

 Returns:
 bool: True if successful, False otherwise
 """
 try:
 # Skip CSV sync if prediction failed
 if prediction_data is None or 'error' in prediction_data:
 print(f" CSV sync skipped: Prediction failed or unavailable")
 return False

 csv_path = os.path.join(os.path.dirname(__file__), '../../Data/water_disease_data.csv')

 # Check if CSV exists
 if not os.path.exists(csv_path):
 print(f" CSV file not found at: {csv_path}")
 return False

 # Parse JSON strings if needed
 symptoms = report_data.get('symptoms', {})
 if isinstance(symptoms, str):
 symptoms = json.loads(symptoms)

 water_metrics = report_data.get('water_metrics', {})
 if isinstance(water_metrics, str):
 water_metrics = json.loads(water_metrics)

 # Build new row matching the CSV structure (0 columns)
 # Helper function to safely convert to int
 def safe_int(value, default=0):
 if value is None:
 return default
 try:
 return int(value)
 except (ValueError, TypeError):
 return default

 # Helper function to safely convert to float
 def safe_float(value, default=0.0):
 if value is None:
 return default
 try:
 return float(value)
 except (ValueError, TypeError):
 return default

 new_row = {
 'district': report_data.get('district') or 'Unknown',
 'region': report_data.get('region') or 'Unknown',
 'latitude': safe_float(report_data.get('latitude'), 0.0),
 'longitude': safe_float(report_data.get('longitude'), 0.0),
 'is_urban': safe_int(report_data.get('is_urban'), 0),
 'population_density': safe_int(report_data.get('population_density'), 000),
 'age': safe_int(report_data.get('age'), 0),
 'gender': report_data.get('gender') or 'Male',
 'water_source': report_data.get('water_source') or 'Tap',
 'water_treatment': report_data.get('water_treatment') or 'None',
 'water_quality_index': safe_float(water_metrics.get('water_quality_index'), 0.0),
 'ph': safe_float(water_metrics.get('ph'), .0),
 'turbidity_ntu': safe_float(water_metrics.get('turbidity_ntu'), .0),
 'dissolved_oxygen_mg_l': safe_float(water_metrics.get('dissolved_oxygen_mg_l'), .0),
 'bod_mg_l': safe_float(water_metrics.get('bod_mg_l'), .0),
 'fecal_coliform_per_00ml': safe_int(water_metrics.get('fecal_coliform_per_00ml'), 0),
 'total_coliform_per_00ml': safe_int(water_metrics.get('total_coliform_per_00ml'), 0),
 'tds_mg_l': safe_float(water_metrics.get('tds_mg_l'), 00.0),
 'nitrate_mg_l': safe_float(water_metrics.get('nitrate_mg_l'), .0),
 'fluoride_mg_l': safe_float(water_metrics.get('fluoride_mg_l'), 0.),
 'arsenic_ug_l': safe_float(water_metrics.get('arsenic_ug_l'), .0),
 'open_defecation_rate': safe_float(report_data.get('open_defecation_rate'), 0.),
 'toilet_access': safe_int(report_data.get('toilet_access'), ),
 'sewage_treatment_pct': safe_float(report_data.get('sewage_treatment_pct'), 0.0),
 'handwashing_practice': report_data.get('handwashing_practice') or 'Sometimes',
 'month': safe_int(report_data.get('month'), datetime.now().month),
 'season': report_data.get('season') or 'Summer',
 'avg_temperature_c': safe_float(report_data.get('avg_temperature_c'), .0),
 'avg_rainfall_mm': safe_float(report_data.get('avg_rainfall_mm'), 00.0),
 'avg_humidity_pct': safe_float(report_data.get('avg_humidity_pct'), 0.0),
 'flooding': safe_int(report_data.get('flooding'), 0),
 'symptom_diarrhea': safe_int(symptoms.get('diarrhea'), 0),
 'symptom_vomiting': safe_int(symptoms.get('vomiting'), 0),
 'symptom_fever': safe_int(symptoms.get('fever'), 0),
 'symptom_abdominal_pain': safe_int(symptoms.get('abdominal_pain'), 0),
 'symptom_dehydration': safe_int(symptoms.get('dehydration'), 0),
 'symptom_jaundice': safe_int(symptoms.get('jaundice'), 0),
 'symptom_bloody_stool': safe_int(symptoms.get('bloody_stool'), 0),
 'symptom_skin_rash': safe_int(symptoms.get('skin_rash'), 0),
 'disease': prediction_data.get('predicted_disease') or 'Unknown'
 }

 # Create DataFrame with single row
 new_df = pd.DataFrame([new_row])

 # Append to CSV (mode='a' for append, header=False to not write column names again)
 new_df.to_csv(csv_path, mode='a', header=False, index=False)

 print(f" CSV sync successful: Added row to {csv_path}")
 return True

 except Exception as e:
 print(f" CSV sync failed: {str(e)}")
 return False
