"""
Bayesian Probability Calculator for Water-Borne Disease Prediction

This script calculates conditional probabilities from training data:
- P(Feature Elevated | High Risk)
- P(High Risk | Feature Elevated) using Bayes' Theorem

Based on WHO and Indian water quality standards.
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime

# WHO and Indian Standards for Water Quality
SAFETY_THRESHOLDS = {
 # Water Quality Parameters (WHO/BIS Standards)
 'fecal_coliform_per_00ml': {
 'safe': 0, # WHO: 0 per 00ml for drinking water
 'elevated': 0, # Any detection is concerning
 'high_risk': 00 # Significant contamination
 },
 'total_coliform_per_00ml': {
 'safe': 0,
 'elevated': 0,
 'high_risk': 00
 },
 'ph': {
 'safe_min': ., # WHO: .-.
 'safe_max': .,
 'elevated_min': .0,
 'elevated_max': .0
 },
 'turbidity_ntu': {
 'safe': , # WHO: < NTU for drinking water
 'elevated': , # BIS: < NTU acceptable
 'high_risk': 0 # Significant turbidity
 },
 'dissolved_oxygen_mg_l': {
 'safe_min': .0, # Good water quality
 'elevated_min': .0, # Moderate
 'high_risk_max': .0 # Poor water quality
 },
 'bod_mg_l': {
 'safe': , # Clean water
 'elevated': , # Moderate pollution
 'high_risk': 0 # High pollution
 },
 'tds_mg_l': {
 'safe': 00, # BIS: <00 acceptable
 'elevated': 00,
 'high_risk': 000 # Poor quality
 },
 'nitrate_mg_l': {
 'safe': 0, # WHO: <0 mg/l
 'elevated': , # BIS: < mg/l
 'high_risk': 0 # Exceeds standards
 },
 'fluoride_mg_l': {
 'safe': .0, # BIS: 0.-. optimal
 'elevated': ., # BIS: <. acceptable
 'high_risk': .0 # Dental/skeletal fluorosis risk
 },
 'arsenic_ug_l': {
 'safe': 0, # WHO: <0 μg/l
 'elevated': 0, # BIS: <0 μg/l (relaxed)
 'high_risk': 00 # Serious health risk
 },
 # Environmental Factors
 'avg_rainfall_mm': {
 'safe': 0,
 'elevated': 0, # Heavy rainfall
 'high_risk': 00 # Extreme rainfall (flooding risk)
 },
 'avg_temperature_c': {
 'safe_min': 0,
 'safe_max': 0,
 'elevated_min': ,
 'elevated_max':
 },
 'avg_humidity_pct': {
 'safe_min': 0,
 'safe_max': 0,
 'elevated_min': 0,
 'elevated_max':
 },
 # Sanitation Indicators
 'open_defecation_rate': {
 'safe': 0., # <0%
 'elevated': 0., # 0%
 'high_risk': 0. # >0%
 },
 'sewage_treatment_pct': {
 'safe': 0., # >0% treated
 'elevated': 0., # 0% treated
 'high_risk': 0. # <0% treated (inverted - lower is worse)
 },
 'population_density': {
 'safe': 000,
 'elevated': 000,
 'high_risk': 0000
 }
}

# Disease risk categories
HIGH_RISK_DISEASES = [
 'Cholera', 'Typhoid', 'Dysentery', 'Hepatitis_A',
 'Hepatitis_E', 'Leptospirosis', 'Giardiasis'
]

def load_training_data(csv_path):
 """Load training data from CSV"""
 try:
 df = pd.read_csv(csv_path)
 print(f" Loaded training data: {len(df)} rows, {len(df.columns)} columns")
 print(f" Columns: {df.columns.tolist()[:0]}...")
 return df
 except FileNotFoundError:
 print(f" Error: File not found at {csv_path}")
 return None
 except Exception as e:
 print(f" Error loading data: {e}")
 return None

def classify_feature_level(value, feature_name, thresholds):
 """Classify a feature value as safe, elevated, or high_risk"""
 if pd.isna(value):
 return 'unknown'

 threshold = thresholds.get(feature_name)
 if not threshold:
 return 'unknown'

 # Handle pH (range-based)
 if feature_name == 'ph':
 if threshold['safe_min'] <= value <= threshold['safe_max']:
 return 'safe'
 elif threshold['elevated_min'] <= value <= threshold['elevated_max']:
 return 'elevated'
 else:
 return 'high_risk'

 # Handle dissolved oxygen (inverted - lower is worse)
 elif feature_name == 'dissolved_oxygen_mg_l':
 if value >= threshold['safe_min']:
 return 'safe'
 elif value >= threshold['elevated_min']:
 return 'elevated'
 else:
 return 'high_risk'

 # Handle sewage treatment (inverted - lower is worse)
 elif feature_name == 'sewage_treatment_pct':
 if value >= threshold['safe']:
 return 'safe'
 elif value >= threshold['elevated']:
 return 'elevated'
 else:
 return 'high_risk'

 # Handle temperature and humidity (range-based)
 elif feature_name in ['avg_temperature_c', 'avg_humidity_pct']:
 if threshold['safe_min'] <= value <= threshold['safe_max']:
 return 'safe'
 elif threshold['elevated_min'] <= value <= threshold['elevated_max']:
 return 'elevated'
 else:
 return 'high_risk'

 # Handle standard thresholds (higher is worse)
 else:
 if value <= threshold['safe']:
 return 'safe'
 elif value <= threshold['elevated']:
 return 'elevated'
 else:
 return 'high_risk'

def calculate_bayesian_probabilities(df):
 """Calculate Bayesian probabilities for all features"""

 # Create high risk indicator
 df['is_high_risk'] = df['disease'].isin(HIGH_RISK_DISEASES).astype(int)

 # Calculate base rates
 total_samples = len(df)
 high_risk_count = df['is_high_risk'].sum()
 p_high_risk = high_risk_count / total_samples
 p_safe = - p_high_risk

 print(f"\n Base Rates:")
 print(f" Total samples: {total_samples:,}")
 print(f" High risk cases: {high_risk_count:,} ({p_high_risk:.%})")
 print(f" Safe cases: {total_samples - high_risk_count:,} ({p_safe:.%})")

 results = {
 'metadata': {
 'generated_at': datetime.now().isoformat(),
 'total_samples': int(total_samples),
 'high_risk_count': int(high_risk_count),
 'safe_count': int(total_samples - high_risk_count),
 'p_high_risk': float(p_high_risk),
 'p_safe': float(p_safe),
 'high_risk_diseases': HIGH_RISK_DISEASES
 },
 'thresholds': SAFETY_THRESHOLDS,
 'conditional_probabilities': {}
 }

 print(f"\n Calculating Bayesian Probabilities...")
 print("=" * 0)

 # Calculate probabilities for each feature
 for feature_name, threshold in SAFETY_THRESHOLDS.items():
 if feature_name not in df.columns:
 print(f" Skipping {feature_name} (not in dataset)")
 continue

 # Classify all values
 df[f'{feature_name}_level'] = df[feature_name].apply(
 lambda x: classify_feature_level(x, feature_name, SAFETY_THRESHOLDS)
 )

 feature_probs = {}

 for level in ['elevated', 'high_risk']:
 # Count occurrences
 feature_elevated = df[f'{feature_name}_level'] == level
 n_feature_elevated = feature_elevated.sum()

 if n_feature_elevated == 0:
 continue

 # P(Feature Elevated)
 p_feature_elevated = n_feature_elevated / total_samples

 # P(Feature Elevated | High Risk)
 n_feature_and_high_risk = ((feature_elevated) & (df['is_high_risk'] == )).sum()
 p_feature_given_high_risk = (
 n_feature_and_high_risk / high_risk_count
 if high_risk_count > 0 else 0
 )

 # P(Feature Elevated | Safe)
 n_feature_and_safe = ((feature_elevated) & (df['is_high_risk'] == 0)).sum()
 safe_count = total_samples - high_risk_count
 p_feature_given_safe = (
 n_feature_and_safe / safe_count
 if safe_count > 0 else 0
 )

 # Bayes' Theorem: P(High Risk | Feature Elevated)
 # P(HR|FE) = P(FE|HR) * P(HR) / P(FE)
 if p_feature_elevated > 0:
 p_high_risk_given_feature = (
 p_feature_given_high_risk * p_high_risk / p_feature_elevated
 )
 else:
 p_high_risk_given_feature = 0

 # Relative Risk: How much more likely is high risk given elevated feature?
 relative_risk = (
 p_high_risk_given_feature / p_high_risk
 if p_high_risk > 0 else 0
 )

 feature_probs[level] = {
 'n_samples': int(n_feature_elevated),
 'p_feature': float(p_feature_elevated),
 'p_feature_given_high_risk': float(p_feature_given_high_risk),
 'p_feature_given_safe': float(p_feature_given_safe),
 'p_high_risk_given_feature': float(p_high_risk_given_feature),
 'relative_risk': float(relative_risk),
 'risk_increase_pct': float((relative_risk - ) * 00)
 }

 if feature_probs:
 results['conditional_probabilities'][feature_name] = feature_probs

 # Print summary for high_risk level
 if 'high_risk' in feature_probs:
 hr = feature_probs['high_risk']
 print(f"\n{feature_name}:")
 print(f" P(High Risk | {level}) = {hr['p_high_risk_given_feature']:.%}")
 print(f" Relative Risk = {hr['relative_risk']:.f}x")
 print(f" Risk Increase = {hr['risk_increase_pct']:+.f}%")

 return results

def save_results(results, output_path):
 """Save results to JSON file"""
 try:
 # Create models directory if it doesn't exist
 output_path.parent.mkdir(parents=True, exist_ok=True)

 with open(output_path, 'w') as f:
 json.dump(results, f, indent=)

 print(f"\n Results saved to: {output_path}")
 return True
 except Exception as e:
 print(f"\n Error saving results: {e}")
 return False

def print_summary(results):
 """Print summary of results"""
 print("\n" + "=" * 0)
 print(" BAYESIAN PROBABILITY CALCULATION SUMMARY")
 print("=" * 0)

 metadata = results['metadata']
 print(f"\nDataset Statistics:")
 print(f" Total samples: {metadata['total_samples']:,}")
 print(f" High risk cases: {metadata['high_risk_count']:,} ({metadata['p_high_risk']:.%})")
 print(f" Safe cases: {metadata['safe_count']:,} ({metadata['p_safe']:.%})")

 print(f"\nHigh Risk Diseases:")
 for disease in metadata['high_risk_diseases']:
 print(f" - {disease}")

 print(f"\nFeatures Analyzed: {len(results['conditional_probabilities'])}")

 # Find top risk factors
 print(f"\n Top Risk Factors (by relative risk):")
 risk_factors = []
 for feature, probs in results['conditional_probabilities'].items():
 if 'high_risk' in probs:
 risk_factors.append((
 feature,
 probs['high_risk']['relative_risk'],
 probs['high_risk']['p_high_risk_given_feature']
 ))

 risk_factors.sort(key=lambda x: x[], reverse=True)
 for i, (feature, rel_risk, prob) in enumerate(risk_factors[:0], ):
 print(f" {i}. {feature}: {rel_risk:.f}x risk ({prob:.%} probability)")

 print("\n" + "=" * 0)
 print(" Bayesian probability calculation complete!")
 print("=" * 0)

def main():
 """Main execution function"""
 print("=" * 0)
 print(" BAYESIAN PROBABILITY CALCULATOR")
 print("=" * 0)

 # Define paths
 script_dir = Path(__file__).parent
 csv_path = script_dir / '../Data/water_disease_data.csv'
 output_path = script_dir / 'models/bayesian_probs.json'

 print(f"\nInput: {csv_path}")
 print(f"Output: {output_path}")

 # Load data
 print(f"\n Loading training data...")
 df = load_training_data(csv_path)
 if df is None:
 return

 # Calculate probabilities
 results = calculate_bayesian_probabilities(df)

 # Save results
 if save_results(results, output_path):
 print_summary(results)

 # Print file size
 file_size = output_path.stat().st_size
 print(f"\nOutput file size: {file_size:,} bytes ({file_size/0:.f} KB)")
 else:
 print("\n Failed to save results")

if __name__ == "__main__":
 main()
