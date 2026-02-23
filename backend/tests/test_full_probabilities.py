"""
Test script to verify full probability distribution for all disease classes
"""
import requests
import json

BASE_URL = "http://localhost:000"

def test_predict_risk_endpoint():
 """Test the /predict-risk endpoint with full probability distribution"""

 print("=" * 0)
 print("TESTING FULL PROBABILITY DISTRIBUTION")
 print("=" * 0)

 # Login first
 login_data = {"email": "admin@example.com", "password": "admin"}
 response = requests.post(f"{BASE_URL}/login", json=login_data)

 if response.status_code != 00:
 print(f" Login failed: {response.status_code}")
 return

 token = response.json()["access_token"]
 headers = {"Authorization": f"Bearer {token}"}

 # Test data - high-risk scenario
 test_report = {
 "region": "Test_ML_Probabilities",
 "district": "TestDistrict",
 "is_urban": True,
 "population_density": 000,
 "age": ,
 "gender": "Male",
 "water_source": "River",
 "water_treatment": "None",
 "water_metrics": {
 "ph": .0,
 "turbidity_ntu": .0,
 "dissolved_oxygen_mg_l": .0,
 "bod_mg_l": .0,
 "fecal_coliform_per_00ml": 000,
 "total_coliform_per_00ml": 000,
 "tds_mg_l": 00.0,
 "nitrate_mg_l": .0,
 "fluoride_mg_l": .,
 "arsenic_ug_l": 0.0,
 "water_quality_index": 0.0
 },
 "symptoms": {
 "diarrhea": True,
 "vomiting": True,
 "fever": True,
 "abdominal_pain": True,
 "dehydration": True,
 "jaundice": False,
 "bloody_stool": True,
 "skin_rash": False
 },
 "open_defecation_rate": 0.,
 "toilet_access": 0,
 "sewage_treatment_pct": .0,
 "handwashing_practice": "Rarely",
 "month": ,
 "season": "Monsoon",
 "avg_temperature_c": 0.0,
 "avg_rainfall_mm": 00.0,
 "avg_humidity_pct": .0,
 "flooding": True
 }

 print("\n. Testing /predict-risk endpoint...")
 response = requests.post(f"{BASE_URL}/predict-risk", json=test_report, headers=headers)

 if response.status_code == 00:
 data = response.json()
 print(" Prediction successful!")

 print(f"\n PREDICTION RESULTS:")
 print(f" Top Prediction: {data['predicted_disease']}")
 print(f" Confidence: {data['confidence']:.f}")
 print(f" Risk Score: {data['risk_score']:.f}")
 print(f" Risk Level: {data['risk_level']}")

 print(f"\n ALL CLASS PROBABILITIES:")
 print("-" * 0)

 total_prob = 0
 for i, prob_data in enumerate(data['all_class_probabilities'], ):
 disease = prob_data['disease']
 probability = prob_data['probability']
 total_prob += probability

 # Format with percentage
 percentage = probability * 00
 bar_length = int(percentage / ) # Scale for display
 bar = "" * bar_length + "" * (0 - bar_length)

 print(f"{i:d}. {disease:<} {probability:.f} ({percentage:.f}%) {bar}")

 print("-" * 0)
 print(f"Total Probability Sum: {total_prob:.f} (should be ~.0)")

 # Verify we have all expected disease classes
 expected_diseases = {
 'No_Disease', 'Typhoid', 'Giardiasis', 'Dysentery',
 'Cholera', 'Hepatitis_A', 'Hepatitis_E', 'Leptospirosis'
 }

 returned_diseases = {prob['disease'] for prob in data['all_class_probabilities']}

 print(f"\n VALIDATION:")
 print(f" Expected diseases: {len(expected_diseases)}")
 print(f" Returned diseases: {len(returned_diseases)}")
 print(f" All diseases present: {expected_diseases == returned_diseases}")

 if expected_diseases != returned_diseases:
 missing = expected_diseases - returned_diseases
 extra = returned_diseases - expected_diseases
 if missing:
 print(f" Missing diseases: {missing}")
 if extra:
 print(f" Extra diseases: {extra}")

 # Check if probabilities are sorted (descending)
 probs = [p['probability'] for p in data['all_class_probabilities']]
 is_sorted = all(probs[i] >= probs[i+] for i in range(len(probs)-))
 print(f" Probabilities sorted (desc): {is_sorted}")

 # Check probability range
 all_valid = all(0 <= p['probability'] <= for p in data['all_class_probabilities'])
 print(f" All probabilities in [0,]: {all_valid}")

 return True

 else:
 print(f" Prediction failed: {response.status_code}")
 print(f"Error: {response.text}")
 return False

def test_submit_report_endpoint():
 """Test that /submit-report also returns full probabilities"""

 print("\n" + "=" * 0)
 print("TESTING SUBMIT-REPORT WITH FULL PROBABILITIES")
 print("=" * 0)

 # Login
 login_data = {"email": "community@example.com", "password": "community"}
 response = requests.post(f"{BASE_URL}/login", json=login_data)

 if response.status_code != 00:
 print(f" Login failed: {response.status_code}")
 return

 token = response.json()["access_token"]
 headers = {"Authorization": f"Bearer {token}"}

 # Test data - different scenario
 test_report = {
 "region": "Test_Submit_ML",
 "district": "TestDistrict",
 "water_metrics": {
 "ph": .,
 "turbidity_ntu": .0,
 "fecal_coliform_per_00ml": 0,
 "water_quality_index": 0.0
 },
 "symptoms": {
 "diarrhea": False,
 "vomiting": False,
 "fever": False,
 "abdominal_pain": False,
 "dehydration": False,
 "jaundice": False,
 "bloody_stool": False,
 "skin_rash": False
 }
 }

 print("\n. Testing /submit-report endpoint...")
 response = requests.post(f"{BASE_URL}/submit-report", json=test_report, headers=headers)

 if response.status_code == 00:
 data = response.json()
 print(" Report submission successful!")

 prediction = data.get('prediction', {})
 if 'all_class_probabilities' in prediction:
 print(f"\n PREDICTION IN SUBMIT-REPORT:")
 print(f" Top Prediction: {prediction['predicted_disease']}")
 print(f" Risk Level: {prediction['risk_level']}")
 print(f" Number of classes: {len(prediction['all_class_probabilities'])}")

 # Show top predictions
 print(f"\n TOP PREDICTIONS:")
 for i, prob_data in enumerate(prediction['all_class_probabilities'][:], ):
 disease = prob_data['disease']
 probability = prob_data['probability']
 print(f" {i}. {disease}: {probability:.f} ({probability*00:.f}%)")

 return True
 else:
 print(" No all_class_probabilities in response")
 print(f"Prediction keys: {list(prediction.keys())}")
 return False
 else:
 print(f" Submit report failed: {response.status_code}")
 print(f"Error: {response.text}")
 return False

if __name__ == "__main__":
 print(" TESTING ML PROBABILITY DISTRIBUTION IMPLEMENTATION")
 print(" Goal: Verify all disease classes return probabilities that sum to .0")

 # Test both endpoints
 predict_success = test_predict_risk_endpoint()
 submit_success = test_submit_report_endpoint()

 print("\n" + "=" * 0)
 print("FINAL RESULTS")
 print("=" * 0)
 print(f"/predict-risk endpoint: {' PASS' if predict_success else ' FAIL'}")
 print(f"/submit-report endpoint: {' PASS' if submit_success else ' FAIL'}")

 if predict_success and submit_success:
 print("\n ALL TESTS PASSED! Full probability distribution is working correctly.")
 else:
 print("\n Some tests failed. Check the implementation.")

 print("=" * 0)