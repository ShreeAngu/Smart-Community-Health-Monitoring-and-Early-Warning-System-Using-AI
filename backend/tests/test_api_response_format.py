"""
Simple test to show the exact API response format for full probabilities
"""
import requests
import json

BASE_URL = "http://localhost:000"

# Login
login_data = {"email": "admin@example.com", "password": "admin"}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Test data
test_report = {
 "region": "API_Test_Region",
 "water_metrics": {
 "ph": .,
 "fecal_coliform_per_00ml": 000,
 "water_quality_index": 0.0
 },
 "symptoms": {
 "diarrhea": True,
 "fever": True,
 "vomiting": False,
 "abdominal_pain": True,
 "dehydration": False,
 "jaundice": False,
 "bloody_stool": False,
 "skin_rash": False
 }
}

print("=" * 0)
print("API RESPONSE FORMAT EXAMPLE")
print("=" * 0)

# Test /predict-risk endpoint
print("\n POST /predict-risk")
print("-" * 0)
response = requests.post(f"{BASE_URL}/predict-risk", json=test_report, headers=headers)

if response.status_code == 00:
 data = response.json()
 print(" Status: 00 OK")
 print("\n Response Schema:")
 print(json.dumps(data, indent=))

 print(f"\n Summary:")
 print(f" - predicted_disease: {data['predicted_disease']}")
 print(f" - confidence: {data['confidence']}")
 print(f" - risk_score: {data['risk_score']}")
 print(f" - risk_level: {data['risk_level']}")
 print(f" - all_class_probabilities: {len(data['all_class_probabilities'])} classes")

 # Verify sum
 total = sum(p['probability'] for p in data['all_class_probabilities'])
 print(f" - probability_sum: {total:.f}")

else:
 print(f" Error: {response.status_code}")
 print(response.text)

print("\n" + "=" * 0)