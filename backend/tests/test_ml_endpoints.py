"""
Comprehensive ML Endpoint Testing Script
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:000"
EMAIL = "community@example.com"
PASSWORD = "community"

def test_ml_endpoints():
 print("=" * 0)
 print("ML ENDPOINTS COMPREHENSIVE TEST")
 print("=" * 0)

 # Login
 print("\n[/] Authenticating...")
 login_response = requests.post(
 f"{BASE_URL}/login",
 json={"email": EMAIL, "password": PASSWORD}
 )

 if login_response.status_code != 00:
 print(f" Login failed: {login_response.status_code}")
 return

 token = login_response.json()["access_token"]
 headers = {"Authorization": f"Bearer {token}"}
 print(f" Authenticated")

 # Submit Report
 print("\n[/] Submitting report with ML prediction...")

 test_report = {
 "region": "Mumbai_Test",
 "district": "Mumbai_Central",
 "is_urban": True,
 "population_density": 000,
 "age": ,
 "gender": "Female",
 "water_source": "Tap",
 "water_treatment": "Chlorination",
 "handwashing_practice": "Always",
 "month": ,
 "season": "Monsoon",
 "flooding": True,
 "symptoms": {
 "diarrhea": True,
 "vomiting": True,
 "fever": True,
 "abdominal_pain": True,
 "dehydration": True,
 "jaundice": False,
 "bloody_stool": False,
 "skin_rash": False
 },
 "water_metrics": {
 "water_quality_index": .0,
 "ph": .,
 "turbidity_ntu": .0,
 "dissolved_oxygen_mg_l": .0,
 "bod_mg_l": .,
 "fecal_coliform_per_00ml": 0,
 "total_coliform_per_00ml": 00,
 "tds_mg_l": 0.0,
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
 return

 result = submit_response.json()
 print(" Report submitted!")

 if result.get('prediction'):
 pred = result['prediction']
 if 'error' not in pred:
 print(f"\n PREDICTION:")
 print(f" Disease: {pred.get('predicted_disease')}")
 print(f" Risk Score: {pred.get('risk_score', 0)*00:.f}%")
 print(f" Risk Level: {pred.get('risk_level')}")
 print(f" Confidence: {pred.get('confidence', 0):.%}")

 # Regional Risk
 print("\n[/] Fetching regional risk...")
 regional_response = requests.get(f"{BASE_URL}/regional-risk", headers=headers)

 if regional_response.status_code == 00:
 risks = regional_response.json().get('regional_risks', {})
 print(f" Retrieved {len(risks)} regions")
 sorted_regions = sorted(risks.items(), key=lambda x: x[]['risk_index'], reverse=True)
 for region, data in sorted_regions[:]:
 print(f" {region}: {data['risk_index']:.f}% ({data['risk_level']})")

 # Feature Importance
 print("\n[/] Fetching feature importance...")
 feature_response = requests.get(f"{BASE_URL}/feature-importance", headers=headers)

 if feature_response.status_code == 00:
 features = feature_response.json().get('top_0_features', [])
 print(f" Top 0 features:")
 for i, feat in enumerate(features[:], ):
 print(f" {i}. {feat['feature']}: {feat['importance_percentage']:.f}%")

 # Alerts
 print("\n[/] Fetching alerts...")
 alerts_response = requests.get(f"{BASE_URL}/alerts", headers=headers)

 if alerts_response.status_code == 00:
 alerts = alerts_response.json()
 print(f" Retrieved {len(alerts)} alert(s)")

 print("\n" + "=" * 0)
 print(" ALL TESTS COMPLETE")
 print("=" * 0)

if __name__ == "__main__":
 test_ml_endpoints()
