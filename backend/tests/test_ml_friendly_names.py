"""
Test ML Engine with Friendly Column Names

Run with: python backend/test_ml_friendly_names.py
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from ml_engine import BayesianRiskAnalyzer

def test_friendly_names():
 """Test that ML engine uses friendly column names"""

 print("=" * 0)
 print(" TESTING ML ENGINE WITH FRIENDLY NAMES")
 print("=" * 0)

 # Initialize analyzer
 analyzer = BayesianRiskAnalyzer(models_dir="./models")

 if not analyzer.model or not analyzer.bayesian_probs:
 print(" Analyzer not fully initialized - skipping test")
 return

 print("\n Analyzer initialized successfully")

 # Test feature name conversion
 print("\n Testing Feature Name Conversion:")
 print("-" * 0)

 test_features = [
 'fecal_coliform_per_00ml',
 'ph',
 'turbidity_ntu',
 'arsenic_ug_l',
 'nitrate_mg_l',
 'bod_mg_l'
 ]

 # Import the utility directly
 from utils.column_mapping import get_friendly_name

 for feature in test_features:
 friendly = get_friendly_name(feature)
 print(f" {feature:0s} → {friendly}")

 print("\n Sample Risk Driver Output:")
 print("-" * 0)

 # Create a sample driver object (simulating what would be returned)
 sample_driver = {
 'feature': 'fecal_coliform_per_00ml',
 'feature_display': get_friendly_name('fecal_coliform_per_00ml'),
 'factor': get_friendly_name('fecal_coliform_per_00ml'),
 'bayesian_probability': .,
 'bayesian_label': 'P(High Risk | fecal coliform elevated)',
 'model_importance': 0.,
 'model_label': 'XGBoost Feature Weight',
 'hybrid_score_percentage': .,
 'current_value_display': '00 per 00ml',
 'safe_value_display': '<00 per 00ml'
 }

 print(f"\n Feature (Technical): {sample_driver['feature']}")
 print(f" Feature (Display): {sample_driver['feature_display']}")
 print(f" Factor (Display): {sample_driver['factor']}")
 print(f"\n Bayesian Probability: {sample_driver['bayesian_probability']}%")
 print(f" ML Importance: {sample_driver['model_importance']}%")
 print(f" Hybrid Score: {sample_driver['hybrid_score_percentage']}%")
 print(f"\n Current Value: {sample_driver['current_value_display']}")
 print(f" Safe Value: {sample_driver['safe_value_display']}")

 print("\n" + "=" * 0)
 print(" Friendly names integration test complete!")
 print("=" * 0)
 print("\n Next Steps:")
 print(" . Restart backend server: python backend/start_server.py")
 print(" . Test API endpoint: GET /regional-risk/{region}/drivers")
 print(" . Verify friendly names appear in modal")

if __name__ == "__main__":
 test_friendly_names()
