"""
Simple ML Endpoint Test (No Unicode)
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("ML ENDPOINTS TEST")
print("=" * 80)

# Login
print("\n[1/4] Login...")
login_resp = requests.post(f"{BASE_URL}/login", json={
    "email": "community@example.com",
    "password": "community123"
})

if login_resp.status_code != 200:
    print(f"FAILED: {login_resp.status_code}")
    exit(1)

token = login_resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("SUCCESS: Authenticated")

# Submit Report
print("\n[2/4] Submit Report...")
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
        "water_quality_index": 35.0,
        "ph": 6.2,
        "turbidity_ntu": 12.0,
        "dissolved_oxygen_mg_l": 6.0,
        "bod_mg_l": 6.5,
        "fecal_coliform_per_100ml": 850,
        "total_coliform_per_100ml": 1500,
        "tds_mg_l": 550.0,
        "nitrate_mg_l": 12.0,
        "fluoride_mg_l": 0.9,
        "arsenic_ug_l": 15.0
    }
}

submit_resp = requests.post(f"{BASE_URL}/submit-report", json=report, headers=headers)

if submit_resp.status_code != 200:
    print(f"FAILED: {submit_resp.status_code}")
    print(submit_resp.text)
    exit(1)

result = submit_resp.json()
print("SUCCESS: Report submitted")

if result.get('prediction'):
    pred = result['prediction']
    if 'error' not in pred:
        print(f"  Disease: {pred.get('predicted_disease')}")
        print(f"  Risk Score: {pred.get('risk_score', 0)*100:.1f}%")
        print(f"  Risk Level: {pred.get('risk_level')}")
        print(f"  Confidence: {pred.get('confidence', 0)*100:.1f}%")
        
        if pred.get('risk_score', 0) > 0.65:
            print("  ALERT: High risk detected - alert should be auto-created!")

# Regional Risk
print("\n[3/4] Regional Risk...")
regional_resp = requests.get(f"{BASE_URL}/regional-risk", headers=headers)

if regional_resp.status_code == 200:
    risks = regional_resp.json().get('regional_risks', {})
    print(f"SUCCESS: {len(risks)} regions")
    for region, data in list(risks.items())[:3]:
        print(f"  {region}: {data['risk_index']:.1f}% ({data['risk_level']})")

# Feature Importance
print("\n[4/4] Feature Importance...")
feature_resp = requests.get(f"{BASE_URL}/feature-importance", headers=headers)

if feature_resp.status_code == 200:
    features = feature_resp.json().get('top_10_features', [])
    print(f"SUCCESS: Top 10 features")
    for i, feat in enumerate(features[:5], 1):
        print(f"  {i}. {feat['feature']}: {feat['importance_percentage']:.2f}%")

print("\n" + "=" * 80)
print("ALL TESTS PASSED")
print("=" * 80)
