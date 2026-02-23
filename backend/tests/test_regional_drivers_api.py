"""
Test script for the regional risk drivers API endpoint
"""

import requests
import json

BASE_URL = "http://localhost:000"

def login_as_admin():
 """Login as admin and get token"""
 response = requests.post(
 f"{BASE_URL}/login",
 json={
 "email": "admin@example.com",
 "password": "admin"
 }
 )

 if response.status_code == 00:
 token = response.json()["access_token"]
 print(f" Login successful")
 return token
 else:
 print(f" Login failed: {response.status_code}")
 print(response.text)
 return None

def login_as_community():
 """Login as community user and get token"""
 response = requests.post(
 f"{BASE_URL}/login",
 json={
 "email": "community@example.com",
 "password": "community"
 }
 )

 if response.status_code == 00:
 token = response.json()["access_token"]
 print(f" Login successful (community)")
 return token
 else:
 print(f" Login failed: {response.status_code}")
 return None

def test_regional_drivers(token, region, days=):
 """Test the regional drivers endpoint"""
 headers = {"Authorization": f"Bearer {token}"}

 response = requests.get(
 f"{BASE_URL}/regional-risk/{region}/drivers?days={days}",
 headers=headers
 )

 if response.status_code == 00:
 data = response.json()
 return data
 else:
 print(f" Error: {response.status_code}")
 print(response.text)
 return None

def print_drivers_analysis(data):
 """Pretty print the drivers analysis"""
 if not data:
 return

 print("\n" + "=" * 0)
 print("REGIONAL RISK DRIVERS ANALYSIS")
 print("=" * 0)

 # Summary
 if 'summary' in data:
 summary = data['summary']
 print(f"\n Region: {summary.get('region')}")
 print(f" Analysis Period: {summary.get('analysis_period_days')} days")
 print(f" Reports Analyzed: {summary.get('reports_analyzed')}")
 print(f" Risk Drivers Identified: {summary.get('risk_drivers_identified')}")

 if summary.get('top_driver'):
 print(f"\n Top Driver: {summary['top_driver']}")
 print(f" Hybrid Score: {summary['top_driver_score']:.f}")

 if summary.get('critical_factors') is not None:
 print(f"\n Critical Factors (score > 0.): {summary['critical_factors']}")

 if summary.get('recommendation'):
 print(f" Recommendation: {summary['recommendation']}")

 if summary.get('message'):
 print(f"\n{summary['message']}")

 # Drivers
 if data.get('drivers'):
 print(f"\n Top {len(data['drivers'])} Risk Drivers:")

 for i, driver in enumerate(data['drivers'], ):
 print(f"\n{i}. {driver['icon']} {driver['feature_display']}")
 print(f" Current Value: {driver['current_value']}")
 print(f" Safe Threshold: {driver['safe_value']}")
 print(f" Risk Level: {driver['risk_level'].upper()}")
 print(f" Hybrid Score: {driver['hybrid_score']:.f}")
 print(f" Bayesian: {driver['bayesian_score']:.f} (0% weight)")
 print(f" ML Importance: {driver['ml_importance']:.f} (0% weight)")
 print(f" Deviation: {driver['deviation_score']:.f} (0% weight)")
 print(f" Samples: {driver['sample_count']}")
 print(f" {driver['recommendation']}")

 # Methodology
 if data.get('methodology'):
 print(f"\n" + "=" * 0)
 print(" METHODOLOGY")
 print("=" * 0)
 method = data['methodology']
 print(f"\n{method['description']}")
 print(f"\nFormula: {method['hybrid_score_formula']}")

 print(f"\nComponents:")
 for comp_name, comp_data in method['components'].items():
 print(f" • {comp_name.replace('_', ' ').title()} ({comp_data['weight']*00:.0f}%)")
 print(f" {comp_data['description']}")

 # Metadata
 if data.get('metadata'):
 print(f"\n" + "=" * 0)
 print(" METADATA")
 print("=" * 0)
 meta = data['metadata']
 print(f"Analyzed At: {meta.get('analyzed_at')}")
 print(f"Total Features Analyzed: {meta.get('total_features_analyzed')}")
 print(f"Base Risk (Population): {meta.get('base_risk', 0):.%}")

def main():
 """Run all tests"""
 print("=" * 0)
 print("TESTING REGIONAL RISK DRIVERS API ENDPOINT")
 print("=" * 0)

 # Test : Admin access
 print("\n" + "=" * 0)
 print("TEST : Admin Access (Should Succeed)")
 print("=" * 0)

 admin_token = login_as_admin()
 if not admin_token:
 print(" Cannot proceed without admin token")
 return

 # Test with Coimbatore North
 print("\n Testing: Coimbatore North ( days)")
 data = test_regional_drivers(admin_token, "Coimbatore North", )
 if data:
 print_drivers_analysis(data)

 # Test with TestRegion
 print("\n\n Testing: TestRegion ( days)")
 data = test_regional_drivers(admin_token, "TestRegion", )
 if data:
 print_drivers_analysis(data)

 # Test : Community user access (should fail)
 print("\n\n" + "=" * 0)
 print("TEST : Community User Access (Should Fail with 0)")
 print("=" * 0)

 community_token = login_as_community()
 if community_token:
 print("\n Testing: Coimbatore North as community user")
 headers = {"Authorization": f"Bearer {community_token}"}
 response = requests.get(
 f"{BASE_URL}/regional-risk/Coimbatore North/drivers?days=",
 headers=headers
 )

 if response.status_code == 0:
 print(" Correctly rejected: 0 Forbidden")
 print(f" Message: {response.json().get('detail')}")
 else:
 print(f" Unexpected status: {response.status_code}")

 # Test : Different time periods
 print("\n\n" + "=" * 0)
 print("TEST : Different Time Periods")
 print("=" * 0)

 for days in [, , ]:
 print(f"\n Testing: Coimbatore North ({days} days)")
 data = test_regional_drivers(admin_token, "Coimbatore North", days)
 if data and data.get('summary'):
 summary = data['summary']
 print(f" Reports: {summary.get('reports_analyzed')}")
 print(f" Drivers: {summary.get('risk_drivers_identified')}")

 print("\n" + "=" * 0)
 print(" All tests complete!")
 print("=" * 0)

if __name__ == "__main__":
 main()
