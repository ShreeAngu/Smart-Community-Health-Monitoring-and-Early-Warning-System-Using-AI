"""
Test the regional-risk API endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Login first
print("=" * 80)
print("TESTING REGIONAL RISK API")
print("=" * 80)

# Login as admin
login_data = {
    "email": "admin@example.com",
    "password": "admin123"
}

print("\n1. Logging in as admin...")
response = requests.post(f"{BASE_URL}/login", json=login_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"✅ Login successful, token: {token[:20]}...")
else:
    print(f"❌ Login failed: {response.status_code}")
    print(response.text)
    exit(1)

# Get regional risk
print("\n2. Fetching regional risk data...")
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/regional-risk", headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Regional risk data retrieved: {len(data)} regions")
    print("\n📊 Regional Risk Summary:")
    print("-" * 80)
    
    for region_data in data:
        print(f"\n🌍 {region_data['region']}")
        print(f"   Risk Index: {region_data['risk_index']}")
        print(f"   Risk Level: {region_data['risk_level']}")
        print(f"   Trend: {region_data['trend']} {region_data['trend_emoji']} ({region_data['trend_percentage']}%)")
        print(f"   Total Predictions: {region_data['total_predictions']}")
        print(f"   Avg Fecal Coliform: {region_data['avg_fecal_coliform']}")
        print(f"   Base Risk: {region_data['base_risk']}")
        if 'lat' in region_data and 'lng' in region_data:
            print(f"   Location: ({region_data['lat']}, {region_data['lng']})")
    
    # Check if Coimbatore North is in the results
    coimbatore = [r for r in data if r['region'] == 'Coimbatore North']
    if coimbatore:
        print("\n" + "=" * 80)
        print("✅ COIMBATORE NORTH FOUND IN RESULTS!")
        print("=" * 80)
        print(json.dumps(coimbatore[0], indent=2))
    else:
        print("\n" + "=" * 80)
        print("❌ COIMBATORE NORTH NOT FOUND IN RESULTS")
        print("=" * 80)
        print("Available regions:", [r['region'] for r in data])
else:
    print(f"❌ Failed to get regional risk: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
