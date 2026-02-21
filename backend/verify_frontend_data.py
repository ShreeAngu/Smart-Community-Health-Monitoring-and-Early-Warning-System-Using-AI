"""
Verification script to show what the frontend should display
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("FRONTEND DATA VERIFICATION")
print("=" * 80)

# Login
login_data = {"email": "admin@example.com", "password": "admin123"}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Get regional risk
response = requests.get(f"{BASE_URL}/regional-risk", headers=headers)
data = response.json()

print("\n📊 WHAT YOU SHOULD SEE ON THE MAP:")
print("=" * 80)

# Define new thresholds
def get_risk_display(risk_index):
    if risk_index < 25:
        return "🟢 LOW (Green)", "Small"
    elif risk_index < 50:
        return "🟡 MEDIUM (Yellow)", "Medium"
    else:
        return "🔴 HIGH (Red)", "Large"

for region_data in sorted(data, key=lambda x: x['risk_index'], reverse=True):
    risk_display, marker_size = get_risk_display(region_data['risk_index'])
    
    print(f"\n📍 {region_data['region']}")
    print(f"   Risk Index: {region_data['risk_index']}%")
    print(f"   Display: {risk_display} marker ({marker_size})")
    print(f"   Trend: {region_data['trend']} {region_data['trend_emoji']}")
    print(f"   Predictions: {region_data['total_predictions']}")
    
    if region_data['region'] == 'Coimbatore North':
        print("\n   ⭐ THIS IS YOUR TEST REGION - Should show as RED! ⭐")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

high_risk = [r for r in data if r['risk_index'] >= 50]
medium_risk = [r for r in data if 25 <= r['risk_index'] < 50]
low_risk = [r for r in data if r['risk_index'] < 25]

print(f"🔴 High Risk Regions (≥50%): {len(high_risk)}")
for r in high_risk:
    print(f"   - {r['region']} ({r['risk_index']}%)")

print(f"\n🟡 Medium Risk Regions (25-50%): {len(medium_risk)}")
for r in medium_risk:
    print(f"   - {r['region']} ({r['risk_index']}%)")

print(f"\n🟢 Low Risk Regions (<25%): {len(low_risk)}")
for r in low_risk:
    print(f"   - {r['region']} ({r['risk_index']}%)")

print("\n" + "=" * 80)
print("✅ If frontend is updated and restarted, you should see:")
print("   - Coimbatore North as a LARGE RED marker")
print("   - TestRegion as a LARGE RED marker")
print("   - Other regions as MEDIUM YELLOW markers")
print("=" * 80)
