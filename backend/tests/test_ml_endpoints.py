"""
Comprehensive ML Endpoint Testing Script
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
EMAIL = "community@example.com"
PASSWORD = "community123"

def test_ml_endpoints():
    print("=" * 80)
    print("ML ENDPOINTS COMPREHENSIVE TEST")
    print("=" * 80)
    
    # Login
    print("\n[1/5] Authenticating...")
    login_response = requests.post(
        f"{BASE_URL}/login",
        json={"email": EMAIL, "password": PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✅ Authenticated")
    
    # Submit Report
    print("\n[2/5] Submitting report with ML prediction...")
    
    test_report = {
        "region": "Mumbai_Test",
        "district": "Mumbai_Central",
        "is_urban": True,
        "population_density": 25000,
        "age": 28,
        "gender": "Female",
        "water_source": "Tap",
        "water_treatment": "Chlorination",
        "handwashing_practice": "Always",
        "month": 7,
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
    
    submit_response = requests.post(
        f"{BASE_URL}/submit-report",
        json=test_report,
        headers=headers
    )
    
    if submit_response.status_code != 200:
        print(f"❌ Submit failed: {submit_response.status_code}")
        return
    
    result = submit_response.json()
    print("✅ Report submitted!")
    
    if result.get('prediction'):
        pred = result['prediction']
        if 'error' not in pred:
            print(f"\n🔬 PREDICTION:")
            print(f"   Disease: {pred.get('predicted_disease')}")
            print(f"   Risk Score: {pred.get('risk_score', 0)*100:.1f}%")
            print(f"   Risk Level: {pred.get('risk_level')}")
            print(f"   Confidence: {pred.get('confidence', 0):.2%}")
    
    # Regional Risk
    print("\n[3/5] Fetching regional risk...")
    regional_response = requests.get(f"{BASE_URL}/regional-risk", headers=headers)
    
    if regional_response.status_code == 200:
        risks = regional_response.json().get('regional_risks', {})
        print(f"✅ Retrieved {len(risks)} regions")
        sorted_regions = sorted(risks.items(), key=lambda x: x[1]['risk_index'], reverse=True)
        for region, data in sorted_regions[:3]:
            print(f"   {region}: {data['risk_index']:.1f}% ({data['risk_level']})")
    
    # Feature Importance
    print("\n[4/5] Fetching feature importance...")
    feature_response = requests.get(f"{BASE_URL}/feature-importance", headers=headers)
    
    if feature_response.status_code == 200:
        features = feature_response.json().get('top_10_features', [])
        print(f"✅ Top 10 features:")
        for i, feat in enumerate(features[:5], 1):
            print(f"   {i}. {feat['feature']}: {feat['importance_percentage']:.2f}%")
    
    # Alerts
    print("\n[5/5] Fetching alerts...")
    alerts_response = requests.get(f"{BASE_URL}/alerts", headers=headers)
    
    if alerts_response.status_code == 200:
        alerts = alerts_response.json()
        print(f"✅ Retrieved {len(alerts)} alert(s)")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_ml_endpoints()
