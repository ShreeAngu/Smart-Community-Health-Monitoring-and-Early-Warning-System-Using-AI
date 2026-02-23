"""
Test the disease distribution in weekly summary endpoint
"""
import requests

BASE_URL = "http://localhost:000"

print("=" * 0)
print("TESTING DISEASE DISTRIBUTION")
print("=" * 0)

# Login
login_data = {"email": "admin@example.com", "password": "admin"}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Get weekly summary
print("\n. Fetching weekly summary...")
response = requests.get(f"{BASE_URL}/reports/weekly", headers=headers)

if response.status_code == 00:
 data = response.json()
 print(f" Weekly summary retrieved")

 print(f"\nTotal Reports: {data.get('total_reports', 0)}")
 print(f"Trend: {data.get('trend', 'N/A')}")

 # Check disease distribution
 disease_dist = data.get('disease_distribution', {})
 by_disease = data.get('by_disease', [])

 print("\n Disease Distribution (dict):")
 if disease_dist:
 for disease, count in sorted(disease_dist.items(), key=lambda x: x[], reverse=True):
 print(f" {disease}: {count}")
 else:
 print(" (empty)")

 print("\n Disease Distribution (list):")
 if by_disease:
 for item in by_disease:
 print(f" {item['disease']}: {item['count']}")
 else:
 print(" (empty)")

 print("\n Top Regions:")
 for region in data.get('by_region', [])[:]:
 print(f" {region['region']}: {region['count']} reports ({region['high_risk_count']} high-risk)")

 print("\n Top Symptoms:")
 for symptom in data.get('by_symptom', [])[:]:
 print(f" {symptom['symptom']}: {symptom['count']}")

else:
 print(f" Failed: {response.status_code}")
 print(response.text)

print("\n" + "=" * 0)
