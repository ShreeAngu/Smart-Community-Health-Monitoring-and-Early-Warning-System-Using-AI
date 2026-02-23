"""
Test API endpoint with friendly column names

This test verifies that the /regional-risk/{region}/drivers endpoint
returns human-readable column names.

Run with: python backend/test_friendly_names_api.py
"""

import requests
import json

def get_auth_token():
 """Get authentication token"""
 base_url = "http://localhost:000"

 try:
 # Try admin login
 response = requests.post(
 f"{base_url}/login",
 json={
 "email": "admin@example.com",
 "password": "admin"
 }
 )

 if response.status_code == 00:
 data = response.json()
 return data.get('access_token')
 else:
 print(f" Login failed: {response.status_code}")
 print(f" Response: {response.text}")
 except Exception as e:
 print(f" Error: {e}")

 return None

def test_api_friendly_names():
 """Test that API returns friendly column names"""

 print("=" * 0)
 print(" TESTING API WITH FRIENDLY COLUMN NAMES")
 print("=" * 0)

 # Get auth token
 print("\n Authenticating...")
 token = get_auth_token()

 if not token:
 print(" Failed to authenticate")
 print(" Make sure backend server is running")
 return

 print(" Authentication successful")

 # API endpoint
 base_url = "http://localhost:000"
 headers = {"Authorization": f"Bearer {token}"}

 # Test regions
 test_regions = ["Coimbatore North", "Chennai", "Madurai"]

 print("\n Testing Regional Drivers API Endpoint")
 print("-" * 0)

 for region in test_regions:
 print(f"\n Testing region: {region}")
 print("-" * 0)

 try:
 # Make API request
 response = requests.get(
 f"{base_url}/regional-risk/{region}/drivers",
 params={"days": },
 headers=headers
 )

 if response.status_code == 00:
 data = response.json()

 print(f" Status: {response.status_code}")
 print(f" Report Count: {data.get('report_count', 0)}")
 print(f" Drivers Found: {len(data.get('drivers', []))}")

 # Check if drivers exist
 drivers = data.get('drivers', [])
 if drivers:
 print(f"\n Top Risk Driver:")
 driver = drivers[0]

 # Display key fields
 print(f" Feature (Technical): {driver.get('feature', 'N/A')}")
 print(f" Feature (Display): {driver.get('feature_display', 'N/A')}")
 print(f" Factor (Display): {driver.get('factor', 'N/A')}")
 print(f"\n Bayesian Probability: {driver.get('bayesian_probability', 0)}%")
 print(f" Bayesian Label: {driver.get('bayesian_label', 'N/A')}")
 print(f"\n ML Importance: {driver.get('model_importance', 0)}%")
 print(f" ML Label: {driver.get('model_label', 'N/A')}")
 print(f"\n Hybrid Score: {driver.get('hybrid_score_percentage', 0)}%")
 print(f" Hybrid Label: {driver.get('hybrid_label', 'N/A')}")
 print(f"\n Current Value: {driver.get('current_value_display', 'N/A')}")
 print(f" Safe Value: {driver.get('safe_value_display', 'N/A')}")

 # Verify friendly names are being used
 feature_display = driver.get('feature_display', '')
 if '_' in feature_display:
 print(f"\n WARNING: Feature display still contains underscores!")
 else:
 print(f"\n Feature display is human-readable")

 # Check Bayesian label
 bayesian_label = driver.get('bayesian_label', '')
 if '_' in bayesian_label and 'P(High Risk' in bayesian_label:
 print(f" WARNING: Bayesian label contains underscores!")
 else:
 print(f" Bayesian label is human-readable")
 else:
 print(f" No drivers found (insufficient data)")

 elif response.status_code == 0:
 print(f" Status: {response.status_code} - No data for region")
 else:
 print(f" Status: {response.status_code}")
 print(f" Error: {response.text}")

 except requests.exceptions.ConnectionError:
 print(f" Connection Error: Backend server not running")
 print(f" Start server with: python backend/start_server.py")
 break
 except Exception as e:
 print(f" Error: {e}")

 print("\n" + "=" * 0)
 print(" API friendly names test complete!")
 print("=" * 0)
 print("\n Expected Results:")
 print(" • feature_display should NOT contain underscores")
 print(" • bayesian_label should use friendly names")
 print(" • All display fields should be human-readable")
 print("\n Example Good Output:")
 print(" Feature (Display): Fecal Bacteria Count")
 print(" Bayesian Label: P(High Risk | Fecal Bacteria Count elevated)")

if __name__ == "__main__":
 test_api_friendly_names()
