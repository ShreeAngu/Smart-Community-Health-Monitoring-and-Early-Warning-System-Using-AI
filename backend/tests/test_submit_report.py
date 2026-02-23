"""
Test script for submit-report endpoint with CSV sync verification
"""
import requests
import json
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:000"
CSV_PATH = "../Data/water_disease_data.csv"

# Test credentials (use existing demo user)
EMAIL = "community@example.com"
PASSWORD = "community"

def get_csv_line_count():
 """Count lines in CSV file"""
 try:
 with open(CSV_PATH, 'r') as f:
 return sum( for _ in f)
 except Exception as e:
 print(f"Error reading CSV: {e}")
 return None

def test_submit_report():
 """Test the submit-report endpoint and verify CSV sync"""

 print("=" * 0)
 print("TESTING SUBMIT-REPORT ENDPOINT WITH CSV SYNC")
 print("=" * 0)

 # Step : Login
 print("\n[/] Logging in...")
 login_response = requests.post(
 f"{BASE_URL}/login",
 json={"email": EMAIL, "password": PASSWORD}
 )

 if login_response.status_code != 00:
 print(f" Login failed: {login_response.status_code}")
 print(login_response.text)
 return

 token = login_response.json()["access_token"]
 print(f" Login successful - Token: {token[:0]}...")

 headers = {"Authorization": f"Bearer {token}"}

 # Step : Count CSV lines before
 print("\n[/] Counting CSV lines before submission...")
 lines_before = get_csv_line_count()
 if lines_before:
 print(f" CSV has {lines_before} lines (including header)")
 else:
 print(" Could not read CSV file")

 # Step : Submit report
 print("\n[/] Submitting test report...")

 test_report = {
 "region": "Test_Region_" + datetime.now().strftime("%H%M%S"),
 "district": "Test_District",
 "is_urban": ,
 "population_density": 000,
 "age": ,
 "gender": "Male",
 "water_source": "Tap",
 "water_treatment": "Chlorination",
 "open_defecation_rate": 0.0,
 "toilet_access": ,
 "sewage_treatment_pct": .0,
 "handwashing_practice": "Always",
 "month": datetime.now().month,
 "season": "Summer",
 "avg_temperature_c": .0,
 "avg_rainfall_mm": 0.0,
 "avg_humidity_pct": .0,
 "flooding": 0,
 "symptoms": {
 "diarrhea": ,
 "vomiting": ,
 "fever": ,
 "abdominal_pain": ,
 "dehydration": 0,
 "jaundice": 0,
 "bloody_stool": 0,
 "skin_rash": 0
 },
 "water_metrics": {
 "water_quality_index": .0,
 "ph": .,
 "turbidity_ntu": .0,
 "dissolved_oxygen_mg_l": .,
 "bod_mg_l": .0,
 "fecal_coliform_per_00ml": 0,
 "total_coliform_per_00ml": 00,
 "tds_mg_l": 00.0,
 "nitrate_mg_l": .0,
 "fluoride_mg_l": 0.,
 "arsenic_ug_l": .0
 }
 }

 submit_response = requests.post(
 f"{BASE_URL}/submit-report",
 json=test_report,
 headers=headers
 )

 if submit_response.status_code != 00:
 print(f" Submit failed: {submit_response.status_code}")
 print(submit_response.text)
 return

 result = submit_response.json()
 print(f" Report submitted successfully!")
 print(f" Report ID: {result['report_id']}")
 print(f" Message: {result['message']}")

 if result.get('prediction'):
 pred = result['prediction']
 if 'error' not in pred:
 print(f" Predicted Disease: {pred.get('predicted_disease')}")
 print(f" Risk Level: {pred.get('risk_level')}")
 print(f" Confidence: {pred.get('confidence', 0):.%}")
 else:
 print(f" Prediction error: {pred.get('error')}")

 # Step : Count CSV lines after
 print("\n[/] Verifying CSV sync...")
 import time
 time.sleep() # Give it a moment to write

 lines_after = get_csv_line_count()
 if lines_after:
 print(f" CSV now has {lines_after} lines")
 if lines_before and lines_after > lines_before:
 print(f" CSV SYNC SUCCESSFUL! Added {lines_after - lines_before} new row(s)")
 elif lines_before:
 print(f" CSV line count unchanged (was {lines_before}, now {lines_after})")
 else:
 print(" CSV updated (baseline count unavailable)")
 else:
 print(" Could not verify CSV after submission")

 print("\n" + "=" * 0)
 print("TEST COMPLETE")
 print("=" * 0)

if __name__ == "__main__":
 test_submit_report()
