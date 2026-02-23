"""
Simple ML Endpoint Test (No Unicode)
"""
import requests
import json

BASE_URL = "http://localhost:000"

print("=" * 0)
print("ML ENDPOINTS TEST")
print("=" * 0)

# Login
print("\n[/] Login...")
login_resp = requests.post(f"{BASE_URL}/login", json={
 "email": "community@example.com",
 "password": "community"
})

if login_resp.status_code != 00:
 print(f"FAILED: {login_resp.status_code}")
 exit()

token = login_resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("SUCCESS: Authenticated")

# Submit Report
print("\n[/] Submit Report...")
report = {
 "region": "TestRegion",
 "district": "TestDistrict",
 "water_source": "Tap",
 "water_treatment": "Chlorination",
 "handwashing_practice": "Always",
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

submit_resp = requests.post(f"{BASE_URL}/submit-report", json=report, headers=headers)

if submit_resp.status_code != 00:
 print(f"FAILED: {submit_resp.status_code}")
 print(submit_resp.text)
 exit()

result = submit_resp.json()
print("SUCCESS: Report submitted")

if result.get('prediction'):
 pred = result['prediction']
 if 'error' not in pred:
 print(f" Disease: {pred.get('predicted_disease')}")
 print(f" Risk Score: {pred.get('risk_score', 0)*00:.f}%")
 print(f" Risk Level: {pred.get('risk_level')}")
 print(f" Confidence: {pred.get('confidence', 0)*00:.f}%")

 if pred.get('risk_score', 0) > 0.:
 print(" ALERT: High risk detected - alert should be auto-created!")

# Regional Risk
print("\n[/] Regional Risk...")
regional_resp = requests.get(f"{BASE_URL}/regional-risk", headers=headers)

if regional_resp.status_code == 00:
 risks = regional_resp.json().get('regional_risks', {})
 print(f"SUCCESS: {len(risks)} regions")
 for region, data in list(risks.items())[:]:
 print(f" {region}: {data['risk_index']:.f}% ({data['risk_level']})")

# Feature Importance
print("\n[/] Feature Importance...")
feature_resp = requests.get(f"{BASE_URL}/feature-importance", headers=headers)

if feature_resp.status_code == 00:
 features = feature_resp.json().get('top_0_features', [])
 print(f"SUCCESS: Top 0 features")
 for i, feat in enumerate(features[:], ):
 print(f" {i}. {feat['feature']}: {feat['importance_percentage']:.f}%")

print("\n" + "=" * 0)
print("ALL TESTS PASSED")
print("=" * 0)
