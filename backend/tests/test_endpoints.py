#!/usr/bin/env python
"""
Comprehensive endpoint testing script for Water-Borne Disease Prediction API
Tests all major endpoints with valid and invalid inputs
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:000"

# Test results tracking
test_results = []

def print_test_header(test_name):
 """Print formatted test header"""
 print("\n" + "=" * 0)
 print(f"TEST: {test_name}")
 print("=" * 0)

def print_result(test_name, passed, details=""):
 """Print and track test result"""
 status = " PASS" if passed else " FAIL"
 print(f"{status} - {test_name}")
 if details:
 print(f" Details: {details}")
 test_results.append((test_name, passed))
 return passed

def test_health_check():
 """Test health check endpoint"""
 print_test_header("Health Check")
 try:
 response = requests.get(f"{BASE_URL}/health")
 passed = response.status_code == 00 and response.json().get("status") == "healthy"
 return print_result("GET /health", passed, f"Status: {response.status_code}")
 except Exception as e:
 return print_result("GET /health", False, str(e))

def test_login_valid():
 """Test login with valid credentials"""
 print_test_header("Login - Valid Credentials")
 try:
 response = requests.post(
 f"{BASE_URL}/login",
 json={"email": "admin@example.com", "password": "admin"}
 )
 passed = response.status_code == 00 and "access_token" in response.json()
 if passed:
 token = response.json()["access_token"]
 return print_result("POST /login (valid)", True, "Token received"), token
 return print_result("POST /login (valid)", False, response.text), None
 except Exception as e:
 return print_result("POST /login (valid)", False, str(e)), None

def test_login_invalid():
 """Test login with invalid credentials"""
 print_test_header("Login - Invalid Credentials")
 try:
 response = requests.post(
 f"{BASE_URL}/login",
 json={"email": "admin@example.com", "password": "wrongpassword"}
 )
 passed = response.status_code == 0
 return print_result("POST /login (invalid)", passed, f"Status: {response.status_code}")
 except Exception as e:
 return print_result("POST /login (invalid)", False, str(e))

def test_submit_report(token):
 """Test submit report endpoint"""
 print_test_header("Submit Health Report")
 try:
 report_data = {
 "region": "Chennai",
 "district": "Chennai",
 "age": 0,
 "gender": "Male",
 "symptoms": {
 "diarrhea": True,
 "vomiting": False,
 "fever": True,
 "abdominal_pain": True,
 "dehydration": False,
 "jaundice": False,
 "bloody_stool": False,
 "skin_rash": False
 },
 "water_metrics": {
 "water_source": "Tap",
 "water_treatment": "Boiling",
 "water_quality_index": .0,
 "ph": .,
 "turbidity_ntu": .
 },
 "is_urban": True,
 "population_density": 000,
 "water_source": "Tap",
 "water_treatment": "Boiling",
 "open_defecation_rate": 0.,
 "toilet_access": ,
 "sewage_treatment_pct": 0.0,
 "handwashing_practice": "Always",
 "month": ,
 "season": "Summer",
 "avg_temperature_c": .0,
 "avg_rainfall_mm": 0.0,
 "avg_humidity_pct": .0,
 "flooding": False
 }

 response = requests.post(
 f"{BASE_URL}/submit-report",
 json=report_data,
 headers={"Authorization": f"Bearer {token}"}
 )
 passed = response.status_code == 00
 details = f"Status: {response.status_code}"
 if passed:
 data = response.json()
 details += f", Report ID: {data.get('report_id')}"
 return print_result("POST /submit-report", passed, details)
 except Exception as e:
 return print_result("POST /submit-report", False, str(e))

def test_predict_risk(token):
 """Test predict risk endpoint"""
 print_test_header("Predict Risk")
 try:
 prediction_data = {
 "region": "Chennai",
 "district": "Chennai",
 "age": ,
 "gender": "Female",
 "symptoms": {
 "diarrhea": True,
 "vomiting": True,
 "fever": True,
 "abdominal_pain": False,
 "dehydration": True,
 "jaundice": False,
 "bloody_stool": False,
 "skin_rash": False
 },
 "water_metrics": {
 "water_source": "Well",
 "water_treatment": "None",
 "water_quality_index": .0,
 "ph": .,
 "turbidity_ntu": .0
 }
 }

 response = requests.post(
 f"{BASE_URL}/predict-risk",
 json=prediction_data,
 headers={"Authorization": f"Bearer {token}"}
 )
 passed = response.status_code == 00
 details = f"Status: {response.status_code}"
 if passed:
 data = response.json()
 details += f", Risk: {data.get('risk_level')}, Score: {data.get('risk_score')}"
 return print_result("POST /predict-risk", passed, details)
 except Exception as e:
 return print_result("POST /predict-risk", False, str(e))

def test_regional_risk(token):
 """Test regional risk endpoint and verify formula"""
 print_test_header("Regional Risk Calculation")
 try:
 response = requests.get(
 f"{BASE_URL}/regional-risk",
 headers={"Authorization": f"Bearer {token}"}
 )
 passed = response.status_code == 00
 details = f"Status: {response.status_code}"

 if passed:
 data = response.json()
 regional_risks = data.get("regional_risks", {})
 formula = data.get("formula", "")

 # Verify formula is present
 expected_formula = "(0. * mean_predicted_risk) + (0. * normalized_fecal_coliform) + (0. * normalized_rainfall) + (0. * flooding_flag)"
 formula_correct = expected_formula in formula

 details += f", Regions: {len(regional_risks)}, Formula: {'' if formula_correct else ''}"

 # Verify at least one region has correct components
 if regional_risks:
 sample_region = list(regional_risks.values())[0]
 has_components = "components" in sample_region
 has_risk_index = "risk_index" in sample_region
 passed = passed and has_components and has_risk_index
 details += f", Components: {'' if has_components else ''}"

 return print_result("GET /regional-risk", passed, details)
 except Exception as e:
 return print_result("GET /regional-risk", False, str(e))

def test_feature_importance(token):
 """Test feature importance endpoint"""
 print_test_header("Feature Importance")
 try:
 response = requests.get(
 f"{BASE_URL}/feature-importance",
 headers={"Authorization": f"Bearer {token}"}
 )
 passed = response.status_code == 00
 details = f"Status: {response.status_code}"

 if passed:
 data = response.json()
 features = data.get("top_0_features", [])
 passed = len(features) == 0
 details += f", Features: {len(features)}/0"
 if features:
 top_feature = features[0]
 details += f", Top: {top_feature.get('feature')}"

 return print_result("GET /feature-importance", passed, details)
 except Exception as e:
 return print_result("GET /feature-importance", False, str(e))

def test_alerts_admin(admin_token):
 """Test alerts endpoint with admin token"""
 print_test_header("Alerts - Admin Access")
 try:
 response = requests.get(
 f"{BASE_URL}/alerts",
 headers={"Authorization": f"Bearer {admin_token}"}
 )
 passed = response.status_code == 00
 details = f"Status: {response.status_code}"

 if passed:
 alerts = response.json()
 details += f", Alerts: {len(alerts)}"

 return print_result("GET /alerts (admin)", passed, details)
 except Exception as e:
 return print_result("GET /alerts (admin)", False, str(e))

def test_alerts_community(community_token):
 """Test alerts endpoint with community token"""
 print_test_header("Alerts - Community Access")
 try:
 response = requests.get(
 f"{BASE_URL}/alerts",
 headers={"Authorization": f"Bearer {community_token}"}
 )
 passed = response.status_code == 00
 details = f"Status: {response.status_code}"

 if passed:
 alerts = response.json()
 details += f", Alerts: {len(alerts)}"

 return print_result("GET /alerts (community)", passed, details)
 except Exception as e:
 return print_result("GET /alerts (community)", False, str(e))

def test_dashboard_stats(token):
 """Test dashboard statistics endpoint"""
 print_test_header("Dashboard Statistics")
 try:
 response = requests.get(
 f"{BASE_URL}/dashboard",
 headers={"Authorization": f"Bearer {token}"}
 )
 passed = response.status_code == 00
 details = f"Status: {response.status_code}"

 if passed:
 data = response.json()
 has_reports = "total_reports" in data
 has_predictions = "total_predictions" in data
 passed = has_reports and has_predictions
 details += f", Reports: {data.get('total_reports', 0)}, Predictions: {data.get('total_predictions', 0)}"

 return print_result("GET /dashboard", passed, details)
 except Exception as e:
 return print_result("GET /dashboard", False, str(e))

def test_unauthorized_access():
 """Test endpoint without token"""
 print_test_header("Unauthorized Access")
 try:
 response = requests.get(f"{BASE_URL}/dashboard")
 passed = response.status_code == 0
 return print_result("GET /dashboard (no token)", passed, f"Status: {response.status_code}")
 except Exception as e:
 return print_result("GET /dashboard (no token)", False, str(e))

def get_community_token():
 """Get community user token"""
 try:
 response = requests.post(
 f"{BASE_URL}/login",
 json={"email": "community@example.com", "password": "community"}
 )
 if response.status_code == 00:
 return response.json()["access_token"]
 except:
 pass
 return None

def print_summary():
 """Print test summary"""
 print("\n" + "=" * 0)
 print("TEST SUMMARY")
 print("=" * 0)

 passed_tests = sum( for _, passed in test_results if passed)
 total_tests = len(test_results)

 print(f"\nTotal Tests: {total_tests}")
 print(f"Passed: {passed_tests}")
 print(f"Failed: {total_tests - passed_tests}")
 print(f"Success Rate: {(passed_tests/total_tests*00):.f}%")

 if passed_tests < total_tests:
 print("\nFailed Tests:")
 for test_name, passed in test_results:
 if not passed:
 print(f" {test_name}")

 print("\n" + "=" * 0)

 if passed_tests == total_tests:
 print(" ALL TESTS PASSED!")
 print("=" * 0)
 return 0
 else:
 print(" SOME TESTS FAILED")
 print("=" * 0)
 return

def main():
 """Run all tests"""
 print("\n" + "=" * 0)
 print("WATER-BORNE DISEASE PREDICTION API - ENDPOINT TESTS")
 print("=" * 0)
 print(f"Base URL: {BASE_URL}")
 print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

 # Test health check
 test_health_check()

 # Test authentication
 test_login_invalid()
 passed, admin_token = test_login_valid()

 if not admin_token:
 print("\n Cannot proceed without admin token")
 return

 # Get community token
 community_token = get_community_token()

 # Test protected endpoints
 test_submit_report(admin_token)
 test_predict_risk(admin_token)
 test_regional_risk(admin_token)
 test_feature_importance(admin_token)
 test_dashboard_stats(admin_token)

 # Test alerts with different roles
 test_alerts_admin(admin_token)
 if community_token:
 test_alerts_community(community_token)

 # Test unauthorized access
 test_unauthorized_access()

 # Print summary
 return print_summary()

if __name__ == "__main__":
 try:
 exit_code = main()
 sys.exit(exit_code)
 except KeyboardInterrupt:
 print("\n\n Tests interrupted by user")
 sys.exit()
 except Exception as e:
 print(f"\n\n Unexpected error: {e}")
 sys.exit()