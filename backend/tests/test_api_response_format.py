"""
Simple test to show the exact API response format for full probabilities
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Login
login_data = {"email": "admin@example.com", "password": "admin123"}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Test data
test_report = {
    "region": "API_Test_Region",
    "water_metrics": {
        "ph": 6.5,
        "fecal_coliform_per_100ml": 1000,
        "water_quality_index": 40.0
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

print("=" * 80)
print("API RESPONSE FORMAT EXAMPLE")
print("=" * 80)

# Test /predict-risk endpoint
print("\n📡 POST /predict-risk")
print("-" * 40)
response = requests.post(f"{BASE_URL}/predict-risk", json=test_report, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("✅ Status: 200 OK")
    print("\n📄 Response Schema:")
    print(json.dumps(data, indent=2))
    
    print(f"\n📊 Summary:")
    print(f"   - predicted_disease: {data['predicted_disease']}")
    print(f"   - confidence: {data['confidence']}")
    print(f"   - risk_score: {data['risk_score']}")
    print(f"   - risk_level: {data['risk_level']}")
    print(f"   - all_class_probabilities: {len(data['all_class_probabilities'])} classes")
    
    # Verify sum
    total = sum(p['probability'] for p in data['all_class_probabilities'])
    print(f"   - probability_sum: {total:.6f}")
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)