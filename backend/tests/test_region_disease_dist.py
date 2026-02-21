"""
Test region-specific disease distribution
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("TESTING REGION-SPECIFIC DISEASE DISTRIBUTION")
print("=" * 80)

# Login
login_data = {"email": "admin@example.com", "password": "admin123"}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Get regional risk with disease distribution
print("\n1. Fetching regional risk data...")
response = requests.get(f"{BASE_URL}/regional-risk", headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Regional risk data retrieved: {len(data)} regions")
    
    for region_data in data:
        print(f"\n{'=' * 80}")
        print(f"🌍 REGION: {region_data['region']}")
        print(f"{'=' * 80}")
        print(f"Risk Index: {region_data['risk_index']}%")
        print(f"Risk Level: {region_data['risk_level']}")
        print(f"Total Predictions: {region_data['total_predictions']}")
        
        disease_dist = region_data.get('disease_distribution', {})
        if disease_dist:
            print(f"\n📊 Disease Distribution:")
            for disease, count in sorted(disease_dist.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / region_data['total_predictions']) * 100
                print(f"   {disease}: {count} ({percentage:.1f}%)")
        else:
            print("\n📊 Disease Distribution: No data")
    
    # Summary
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    
    total_regions_with_diseases = sum(1 for r in data if r.get('disease_distribution'))
    print(f"Regions with disease data: {total_regions_with_diseases}/{len(data)}")
    
    # All diseases across all regions
    all_diseases = set()
    for r in data:
        if r.get('disease_distribution'):
            all_diseases.update(r['disease_distribution'].keys())
    
    print(f"\nUnique diseases detected: {len(all_diseases)}")
    for disease in sorted(all_diseases):
        print(f"  - {disease}")
    
else:
    print(f"❌ Failed: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
