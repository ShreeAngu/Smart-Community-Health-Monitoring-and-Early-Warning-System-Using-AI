"""
Verification script to show what the frontend should display
"""
import requests
import json

BASE_URL = "http://localhost:000"

print("=" * 0)
print("FRONTEND DATA VERIFICATION")
print("=" * 0)

# Login
login_data = {"email": "admin@example.com", "password": "admin"}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Get regional risk
response = requests.get(f"{BASE_URL}/regional-risk", headers=headers)
data = response.json()

print("\n WHAT YOU SHOULD SEE ON THE MAP:")
print("=" * 0)

# Define new thresholds
def get_risk_display(risk_index):
 if risk_index < :
 return " LOW (Green)", "Small"
 elif risk_index < 0:
 return " MEDIUM (Yellow)", "Medium"
 else:
 return " HIGH (Red)", "Large"

for region_data in sorted(data, key=lambda x: x['risk_index'], reverse=True):
 risk_display, marker_size = get_risk_display(region_data['risk_index'])

 print(f"\n {region_data['region']}")
 print(f" Risk Index: {region_data['risk_index']}%")
 print(f" Display: {risk_display} marker ({marker_size})")
 print(f" Trend: {region_data['trend']} {region_data['trend_emoji']}")
 print(f" Predictions: {region_data['total_predictions']}")

 if region_data['region'] == 'Coimbatore North':
 print("\n THIS IS YOUR TEST REGION - Should show as RED! ")

print("\n" + "=" * 0)
print("SUMMARY")
print("=" * 0)

high_risk = [r for r in data if r['risk_index'] >= 0]
medium_risk = [r for r in data if <= r['risk_index'] < 0]
low_risk = [r for r in data if r['risk_index'] < ]

print(f" High Risk Regions (≥0%): {len(high_risk)}")
for r in high_risk:
 print(f" - {r['region']} ({r['risk_index']}%)")

print(f"\n Medium Risk Regions (-0%): {len(medium_risk)}")
for r in medium_risk:
 print(f" - {r['region']} ({r['risk_index']}%)")

print(f"\n Low Risk Regions (<%): {len(low_risk)}")
for r in low_risk:
 print(f" - {r['region']} ({r['risk_index']}%)")

print("\n" + "=" * 0)
print(" If frontend is updated and restarted, you should see:")
print(" - Coimbatore North as a LARGE RED marker")
print(" - TestRegion as a LARGE RED marker")
print(" - Other regions as MEDIUM YELLOW markers")
print("=" * 0)
