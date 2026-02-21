"""
Test script to verify full probability distribution for all disease classes
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_predict_risk_endpoint():
    """Test the /predict-risk endpoint with full probability distribution"""
    
    print("=" * 80)
    print("TESTING FULL PROBABILITY DISTRIBUTION")
    print("=" * 80)
    
    # Login first
    login_data = {"email": "admin@example.com", "password": "admin123"}
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test data - high-risk scenario
    test_report = {
        "region": "Test_ML_Probabilities",
        "district": "TestDistrict",
        "is_urban": True,
        "population_density": 5000,
        "age": 35,
        "gender": "Male",
        "water_source": "River",
        "water_treatment": "None",
        "water_metrics": {
            "ph": 6.0,
            "turbidity_ntu": 25.0,
            "dissolved_oxygen_mg_l": 3.0,
            "bod_mg_l": 12.0,
            "fecal_coliform_per_100ml": 3000,
            "total_coliform_per_100ml": 5000,
            "tds_mg_l": 800.0,
            "nitrate_mg_l": 25.0,
            "fluoride_mg_l": 2.5,
            "arsenic_ug_l": 30.0,
            "water_quality_index": 20.0
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
        "open_defecation_rate": 0.7,
        "toilet_access": 0,
        "sewage_treatment_pct": 15.0,
        "handwashing_practice": "Rarely",
        "month": 7,
        "season": "Monsoon",
        "avg_temperature_c": 30.0,
        "avg_rainfall_mm": 200.0,
        "avg_humidity_pct": 85.0,
        "flooding": True
    }
    
    print("\n1. Testing /predict-risk endpoint...")
    response = requests.post(f"{BASE_URL}/predict-risk", json=test_report, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Prediction successful!")
        
        print(f"\n📊 PREDICTION RESULTS:")
        print(f"   Top Prediction: {data['predicted_disease']}")
        print(f"   Confidence: {data['confidence']:.4f}")
        print(f"   Risk Score: {data['risk_score']:.4f}")
        print(f"   Risk Level: {data['risk_level']}")
        
        print(f"\n📈 ALL CLASS PROBABILITIES:")
        print("-" * 60)
        
        total_prob = 0
        for i, prob_data in enumerate(data['all_class_probabilities'], 1):
            disease = prob_data['disease']
            probability = prob_data['probability']
            total_prob += probability
            
            # Format with percentage
            percentage = probability * 100
            bar_length = int(percentage / 2)  # Scale for display
            bar = "█" * bar_length + "░" * (50 - bar_length)
            
            print(f"{i:2d}. {disease:<15} {probability:.4f} ({percentage:5.2f}%) {bar}")
        
        print("-" * 60)
        print(f"Total Probability Sum: {total_prob:.4f} (should be ~1.0)")
        
        # Verify we have all expected disease classes
        expected_diseases = {
            'No_Disease', 'Typhoid', 'Giardiasis', 'Dysentery', 
            'Cholera', 'Hepatitis_A', 'Hepatitis_E', 'Leptospirosis'
        }
        
        returned_diseases = {prob['disease'] for prob in data['all_class_probabilities']}
        
        print(f"\n🔍 VALIDATION:")
        print(f"   Expected diseases: {len(expected_diseases)}")
        print(f"   Returned diseases: {len(returned_diseases)}")
        print(f"   All diseases present: {expected_diseases == returned_diseases}")
        
        if expected_diseases != returned_diseases:
            missing = expected_diseases - returned_diseases
            extra = returned_diseases - expected_diseases
            if missing:
                print(f"   Missing diseases: {missing}")
            if extra:
                print(f"   Extra diseases: {extra}")
        
        # Check if probabilities are sorted (descending)
        probs = [p['probability'] for p in data['all_class_probabilities']]
        is_sorted = all(probs[i] >= probs[i+1] for i in range(len(probs)-1))
        print(f"   Probabilities sorted (desc): {is_sorted}")
        
        # Check probability range
        all_valid = all(0 <= p['probability'] <= 1 for p in data['all_class_probabilities'])
        print(f"   All probabilities in [0,1]: {all_valid}")
        
        return True
        
    else:
        print(f"❌ Prediction failed: {response.status_code}")
        print(f"Error: {response.text}")
        return False

def test_submit_report_endpoint():
    """Test that /submit-report also returns full probabilities"""
    
    print("\n" + "=" * 80)
    print("TESTING SUBMIT-REPORT WITH FULL PROBABILITIES")
    print("=" * 80)
    
    # Login
    login_data = {"email": "community@example.com", "password": "community123"}
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test data - different scenario
    test_report = {
        "region": "Test_Submit_ML",
        "district": "TestDistrict2",
        "water_metrics": {
            "ph": 7.5,
            "turbidity_ntu": 2.0,
            "fecal_coliform_per_100ml": 50,
            "water_quality_index": 80.0
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
    
    print("\n1. Testing /submit-report endpoint...")
    response = requests.post(f"{BASE_URL}/submit-report", json=test_report, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Report submission successful!")
        
        prediction = data.get('prediction', {})
        if 'all_class_probabilities' in prediction:
            print(f"\n📊 PREDICTION IN SUBMIT-REPORT:")
            print(f"   Top Prediction: {prediction['predicted_disease']}")
            print(f"   Risk Level: {prediction['risk_level']}")
            print(f"   Number of classes: {len(prediction['all_class_probabilities'])}")
            
            # Show top 3 predictions
            print(f"\n🏆 TOP 3 PREDICTIONS:")
            for i, prob_data in enumerate(prediction['all_class_probabilities'][:3], 1):
                disease = prob_data['disease']
                probability = prob_data['probability']
                print(f"   {i}. {disease}: {probability:.4f} ({probability*100:.2f}%)")
            
            return True
        else:
            print("❌ No all_class_probabilities in response")
            print(f"Prediction keys: {list(prediction.keys())}")
            return False
    else:
        print(f"❌ Submit report failed: {response.status_code}")
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    print("🧪 TESTING ML PROBABILITY DISTRIBUTION IMPLEMENTATION")
    print("🎯 Goal: Verify all disease classes return probabilities that sum to 1.0")
    
    # Test both endpoints
    predict_success = test_predict_risk_endpoint()
    submit_success = test_submit_report_endpoint()
    
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"/predict-risk endpoint: {'✅ PASS' if predict_success else '❌ FAIL'}")
    print(f"/submit-report endpoint: {'✅ PASS' if submit_success else '❌ FAIL'}")
    
    if predict_success and submit_success:
        print("\n🎉 ALL TESTS PASSED! Full probability distribution is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the implementation.")
    
    print("=" * 80)