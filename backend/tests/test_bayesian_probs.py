"""
Test script to demonstrate using Bayesian probabilities for risk assessment
"""

import json
from pathlib import Path

def load_bayesian_probs():
 """Load pre-calculated Bayesian probabilities"""
 probs_path = Path(__file__).parent / 'models/bayesian_probs.json'

 try:
 with open(probs_path, 'r') as f:
 data = json.load(f)
 print(f" Loaded Bayesian probabilities from {probs_path}")
 return data
 except FileNotFoundError:
 print(f" File not found: {probs_path}")
 print(" Run 'python calculate_bayesian_probs.py' first")
 return None
 except Exception as e:
 print(f" Error loading probabilities: {e}")
 return None

def assess_water_quality_risk(water_metrics, bayesian_data):
 """
 Assess risk based on water quality metrics using Bayesian probabilities

 Args:
 water_metrics: dict with water quality measurements
 bayesian_data: pre-calculated Bayesian probabilities

 Returns:
 dict with risk assessment
 """
 thresholds = bayesian_data['thresholds']
 cond_probs = bayesian_data['conditional_probabilities']
 base_risk = bayesian_data['metadata']['p_high_risk']

 risk_factors = []
 total_risk_increase = 0

 print("\n" + "=" * 0)
 print(" BAYESIAN RISK ASSESSMENT")
 print("=" * 0)
 print(f"\nBase Risk (Population): {base_risk:.%}")
 print(f"\nWater Quality Metrics:")

 for feature, value in water_metrics.items():
 if feature not in thresholds or feature not in cond_probs:
 continue

 threshold = thresholds[feature]

 # Determine risk level
 if feature == 'fecal_coliform_per_00ml':
 if value >= threshold['high_risk']:
 level = 'high_risk'
 elif value >= threshold['elevated']:
 level = 'elevated'
 else:
 level = 'safe'
 elif feature == 'ph':
 if threshold['safe_min'] <= value <= threshold['safe_max']:
 level = 'safe'
 elif threshold['elevated_min'] <= value <= threshold['elevated_max']:
 level = 'elevated'
 else:
 level = 'high_risk'
 else:
 # Standard threshold logic
 if value <= threshold.get('safe', 0):
 level = 'safe'
 elif value <= threshold.get('elevated', float('inf')):
 level = 'elevated'
 else:
 level = 'high_risk'

 # Get Bayesian probability for this level
 if level in cond_probs[feature]:
 prob_data = cond_probs[feature][level]
 p_high_risk_given_feature = prob_data['p_high_risk_given_feature']
 relative_risk = prob_data['relative_risk']
 risk_increase = prob_data['risk_increase_pct']

 status_icon = "" if level == 'high_risk' else "" if level == 'elevated' else ""
 print(f" {status_icon} {feature}: {value} ({level})")
 print(f" P(High Risk | {level}) = {p_high_risk_given_feature:.%}")
 print(f" Relative Risk = {relative_risk:.f}x ({risk_increase:+.f}%)")

 if level in ['elevated', 'high_risk']:
 risk_factors.append({
 'feature': feature,
 'value': value,
 'level': level,
 'probability': p_high_risk_given_feature,
 'relative_risk': relative_risk,
 'risk_increase_pct': risk_increase
 })
 total_risk_increase += risk_increase

 # Calculate combined risk (simplified - assumes independence)
 # In reality, features are correlated, so this is an upper bound
 combined_risk = min(base_risk * ( + total_risk_increase / 00), .0)

 print("\n" + "=" * 0)
 print(" RISK SUMMARY")
 print("=" * 0)
 print(f"\nRisk Factors Detected: {len(risk_factors)}")
 print(f"Total Risk Increase: {total_risk_increase:+.f}%")
 print(f"Combined Risk Estimate: {combined_risk:.%}")

 if combined_risk >= 0.:
 risk_level = "CRITICAL"
 recommendation = "Immediate action required. Do not use water source."
 elif combined_risk >= 0.:
 risk_level = "HIGH"
 recommendation = "High contamination risk. Water treatment essential."
 elif combined_risk >= 0.:
 risk_level = "MODERATE"
 recommendation = "Moderate risk. Boil water before consumption."
 else:
 risk_level = "LOW"
 recommendation = "Low risk. Standard precautions recommended."

 print(f"\nRisk Level: {risk_level}")
 print(f"Recommendation: {recommendation}")

 # Top risk factors
 if risk_factors:
 print(f"\n Top Risk Factors:")
 risk_factors.sort(key=lambda x: x['relative_risk'], reverse=True)
 for i, factor in enumerate(risk_factors[:], ):
 print(f" {i}. {factor['feature']}: {factor['relative_risk']:.f}x risk")

 return {
 'base_risk': base_risk,
 'combined_risk': combined_risk,
 'risk_level': risk_level,
 'recommendation': recommendation,
 'risk_factors': risk_factors,
 'total_risk_increase_pct': total_risk_increase
 }

def main():
 """Test Bayesian probability assessment"""
 print("=" * 0)
 print(" BAYESIAN PROBABILITY TEST")
 print("=" * 0)

 # Load Bayesian probabilities
 bayesian_data = load_bayesian_probs()
 if not bayesian_data:
 return

 # Test Case : High-risk water source
 print("\n" + "=" * 0)
 print("TEST CASE : High-Risk Water Source (Contaminated River)")
 print("=" * 0)

 high_risk_water = {
 'fecal_coliform_per_00ml': 000,
 'total_coliform_per_00ml': 000,
 'ph': .,
 'turbidity_ntu': ,
 'dissolved_oxygen_mg_l': .0,
 'bod_mg_l': ,
 'tds_mg_l': 00,
 'nitrate_mg_l': ,
 'fluoride_mg_l': .,
 'arsenic_ug_l': 0,
 'avg_rainfall_mm': 00,
 'avg_humidity_pct': ,
 'open_defecation_rate': 0.,
 'sewage_treatment_pct': 0.
 }

 result = assess_water_quality_risk(high_risk_water, bayesian_data)

 # Test Case : Low-risk water source
 print("\n\n" + "=" * 0)
 print("TEST CASE : Low-Risk Water Source (Treated Municipal Water)")
 print("=" * 0)

 low_risk_water = {
 'fecal_coliform_per_00ml': 0,
 'total_coliform_per_00ml': 0,
 'ph': .,
 'turbidity_ntu': 0.,
 'dissolved_oxygen_mg_l': .,
 'bod_mg_l': .,
 'tds_mg_l': 0,
 'nitrate_mg_l': ,
 'fluoride_mg_l': 0.,
 'arsenic_ug_l': ,
 'avg_rainfall_mm': 0,
 'avg_humidity_pct': ,
 'open_defecation_rate': 0.0,
 'sewage_treatment_pct': 0.
 }

 result = assess_water_quality_risk(low_risk_water, bayesian_data)

 # Summary
 print("\n\n" + "=" * 0)
 print(" COMPARISON SUMMARY")
 print("=" * 0)
 print(f"\nTest Case (Contaminated):")
 print(f" Combined Risk: {result['combined_risk']:.%}")
 print(f" Risk Level: {result['risk_level']}")
 print(f" Risk Factors: {len(result['risk_factors'])}")

 print(f"\nTest Case (Treated):")
 print(f" Combined Risk: {result['combined_risk']:.%}")
 print(f" Risk Level: {result['risk_level']}")
 print(f" Risk Factors: {len(result['risk_factors'])}")

 print("\n" + "=" * 0)
 print(" Bayesian probability test complete!")
 print("=" * 0)

if __name__ == "__main__":
 main()
