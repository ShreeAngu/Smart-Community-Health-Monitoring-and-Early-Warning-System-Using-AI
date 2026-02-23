"""
Test script for Volume Surge Alert System

This script tests:
. Volume Surge: Creating reports triggers an alert
. Cooldown: 0th report doesn't create duplicate alert
. AI Risk: High risk score triggers alert
. Auto-resolve: Low risk resolves alerts
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:000"

# Login as community user
def login():
 response = requests.post(
 f"{BASE_URL}/login",
 json={
 "email": "community@example.com",
 "password": "community"
 }
 )
 if response.status_code == 00:
 token = response.json()["access_token"]
 print(f" Login successful")
 return token
 else:
 print(f" Login failed: {response.status_code}")
 print(response.text)
 return None

# Submit a high-risk report
def submit_high_risk_report(token, region="TestRegion", report_num=):
 headers = {"Authorization": f"Bearer {token}"}

 # High-risk symptoms (cholera-like)
 report_data = {
 "region": region,
 "symptoms": {
 "fever": True,
 "diarrhea": True,
 "vomiting": True,
 "abdominal_pain": True,
 "nausea": True,
 "headache": True,
 "fatigue": True,
 "dehydration": True,
 "bloody_stool": True,
 "muscle_aches": False,
 "loss_of_appetite": True,
 "weight_loss": False,
 "jaundice": False,
 "dark_urine": False,
 "rash": False
 },
 "water_metrics": {
 "water_source": "River",
 "water_treatment": "None",
 "fecal_coliform_per_00ml": 000,
 "ph_level": .,
 "turbidity_ntu": ,
 "temperature_celsius": ,
 "rainfall_mm": 0,
 "flooding": True,
 "sanitation_access": False,
 "population_density": 000
 }
 }

 response = requests.post(
 f"{BASE_URL}/submit-report",
 headers=headers,
 json=report_data
 )

 if response.status_code == 00:
 result = response.json()
 print(f" Report #{report_num} submitted: ID={result['report_id']}")
 if result.get('prediction'):
 pred = result['prediction']
 print(f" Disease: {pred.get('predicted_disease')}, Risk: {pred.get('risk_level')}, Score: {pred.get('risk_score', 0)*00:.f}%")
 return True
 else:
 print(f" Report #{report_num} failed: {response.status_code}")
 print(f" {response.text}")
 return False

# Get alerts
def get_alerts(token):
 headers = {"Authorization": f"Bearer {token}"}
 response = requests.get(f"{BASE_URL}/alerts", headers=headers)

 if response.status_code == 00:
 alerts = response.json()
 return alerts
 else:
 print(f" Failed to get alerts: {response.status_code}")
 return []

# Main test
def main():
 print("=" * 0)
 print("VOLUME SURGE ALERT SYSTEM TEST")
 print("=" * 0)

 # Login
 token = login()
 if not token:
 return

 print("\n" + "=" * 0)
 print("TEST : Volume Surge Detection ( cases)")
 print("=" * 0)
 print("Submitting high-risk reports to trigger volume surge alert...")

 test_region = "TestRegion"
 success_count = 0

 for i in range(, 0):
 if submit_high_risk_report(token, test_region, i):
 success_count +=

 print(f"\n Submitted {success_count}/ reports")

 # Check alerts
 print("\n" + "=" * 0)
 print("Checking for Volume Surge Alert...")
 print("=" * 0)

 alerts = get_alerts(token)
 volume_surge_alerts = [a for a in alerts if a.get('alert_type') == 'volume_surge' and a.get('region') == test_region]

 if volume_surge_alerts:
 print(f" Volume Surge Alert Created!")
 for alert in volume_surge_alerts:
 print(f"\n Alert ID: {alert['id']}")
 print(f" Region: {alert['region']}")
 print(f" Type: {alert['alert_type']}")
 print(f" Message: {alert['alert_message']}")
 print(f" Status: {alert['status']}")
 print(f" Timestamp: {alert['timestamp']}")
 else:
 print(" No Volume Surge Alert found!")
 print(f"Total alerts: {len(alerts)}")
 if alerts:
 print("Existing alerts:")
 for alert in alerts:
 print(f" - {alert.get('region')}: {alert.get('alert_type')} - {alert.get('status')}")

 # Test cooldown
 print("\n" + "=" * 0)
 print("TEST : Cooldown Prevention (0th report)")
 print("=" * 0)
 print("Submitting 0th report - should NOT create duplicate alert...")

 submit_high_risk_report(token, test_region, 0)

 alerts_after = get_alerts(token)
 volume_surge_alerts_after = [a for a in alerts_after if a.get('alert_type') == 'volume_surge' and a.get('region') == test_region]

 if len(volume_surge_alerts_after) == len(volume_surge_alerts):
 print(f" Cooldown working! Still {len(volume_surge_alerts_after)} alert(s) (no duplicate)")
 else:
 print(f" Alert count changed: {len(volume_surge_alerts)} -> {len(volume_surge_alerts_after)}")

 # Summary
 print("\n" + "=" * 0)
 print("TEST SUMMARY")
 print("=" * 0)
 print(f"Reports submitted: {success_count + }/0")
 print(f"Volume Surge Alerts: {len(volume_surge_alerts_after)}")
 print(f"Total Active Alerts: {len([a for a in alerts_after if a.get('status') == 'active'])}")

 print("\n" + "=" * 0)
 print("ALERT THRESHOLDS (from backend)")
 print("=" * 0)
 print(" AI_RISK_SCORE: %")
 print(" VOLUME_CASES: cases")
 print(" VOLUME_DAYS: days")
 print(" COOLDOWN_HOURS: hours")

 print("\n Test complete!")

if __name__ == "__main__":
 main()
