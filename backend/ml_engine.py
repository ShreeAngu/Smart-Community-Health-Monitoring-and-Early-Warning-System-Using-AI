"""
ML Engine for Regional Risk Analysis

This module provides Bayesian-enhanced regional risk analysis by combining:
. Bayesian conditional probabilities (from training data)
. ML model feature importance (from XGBoost)
. Regional environmental data (from database)

The hybrid approach provides interpretable, actionable risk drivers.
"""

import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

# Import models (will be available when used in main.py)
try:
 import models
except ImportError:
 models = None
 print(" Models not imported - ml_engine.py running standalone")

# Import column mapping utility
try:
 from utils.column_mapping import get_friendly_name
except ImportError:
 # Fallback if import fails
 def get_friendly_name(column_name: str) -> str:
 return column_name.replace('_', ' ').title()

class BayesianRiskAnalyzer:
 """
 Hybrid risk analyzer combining Bayesian probabilities with ML feature importance
 """

 def __init__(self, models_dir: str = "./models"):
 """
 Initialize the risk analyzer by loading all required artifacts

 Args:
 models_dir: Directory containing model files
 """
 self.models_dir = Path(models_dir)
 self.model = None
 self.scaler = None
 self.label_encoder = None
 self.feature_names = None
 self.preprocessing_info = None
 self.feature_importance = None
 self.bayesian_probs = None

 print("=" * 0)
 print(" Initializing Bayesian Risk Analyzer")
 print("=" * 0)

 # Load all artifacts
 self._load_ml_model()
 self._load_bayesian_probabilities()

 if self.model and self.bayesian_probs:
 print(" Bayesian Risk Analyzer initialized successfully!")
 else:
 print(" Bayesian Risk Analyzer initialized with missing components")
 print("=" * 0)

 def _load_ml_model(self):
 """Load XGBoost model and preprocessors"""
 try:
 # Load model
 model_path = self.models_dir / "best_model.pkl"
 if model_path.exists():
 self.model = joblib.load(model_path)
 print(f" Model loaded: {model_path}")
 else:
 print(f" Model not found: {model_path}")
 return

 # Load scaler
 scaler_path = self.models_dir / "scaler.pkl"
 if scaler_path.exists():
 self.scaler = joblib.load(scaler_path)
 print(f" Scaler loaded: {scaler_path}")

 # Load label encoder
 encoder_path = self.models_dir / "label_encoder.pkl"
 if encoder_path.exists():
 self.label_encoder = joblib.load(encoder_path)
 print(f" Label encoder loaded: {encoder_path}")

 # Load feature names
 feature_names_path = self.models_dir / "feature_names.pkl"
 if feature_names_path.exists():
 self.feature_names = joblib.load(feature_names_path)
 print(f" Feature names loaded: {len(self.feature_names)} features")

 # Load preprocessing info
 preprocessing_path = self.models_dir / "preprocessing_info.pkl"
 if preprocessing_path.exists():
 self.preprocessing_info = joblib.load(preprocessing_path)
 print(f" Preprocessing info loaded")

 # Extract feature importance
 if hasattr(self.model, 'feature_importances_') and self.feature_names:
 self.feature_importance = pd.DataFrame({
 'feature': self.feature_names,
 'importance': self.model.feature_importances_
 }).sort_values('importance', ascending=False)
 print(f" Feature importance extracted: {len(self.feature_importance)} features")
 else:
 print(" Could not extract feature importance")

 except Exception as e:
 print(f" Error loading ML model: {e}")
 import traceback
 traceback.print_exc()

 def _load_bayesian_probabilities(self):
 """Load pre-calculated Bayesian probabilities"""
 try:
 bayesian_path = self.models_dir / "bayesian_probs.json"
 if bayesian_path.exists():
 with open(bayesian_path, 'r') as f:
 self.bayesian_probs = json.load(f)

 n_features = len(self.bayesian_probs.get('conditional_probabilities', {}))
 print(f" Bayesian probabilities loaded: {n_features} features")
 print(f" Base risk: {self.bayesian_probs['metadata']['p_high_risk']:.%}")
 else:
 print(f" Bayesian probabilities not found: {bayesian_path}")
 print(" Run 'python calculate_bayesian_probs.py' to generate")

 except Exception as e:
 print(f" Error loading Bayesian probabilities: {e}")
 import traceback
 traceback.print_exc()

 def get_regional_drivers(
 self,
 db: Session,
 region: str,
 days: int =
 ) -> Dict:
 """
 Analyze regional risk drivers using hybrid Bayesian-ML approach

 Args:
 db: Database session
 region: Region name to analyze
 days: Number of days to look back

 Returns:
 Dictionary with top risk drivers, recommendations, and metadata
 """
 if not self.model or not self.bayesian_probs:
 return {
 'error': 'Risk analyzer not fully initialized',
 'drivers': [],
 'metadata': {}
 }

 try:
 # Query reports for the region
 cutoff_date = datetime.now() - timedelta(days=days)
 reports = db.query(models.Report).filter(
 models.Report.region == region,
 models.Report.timestamp >= cutoff_date
 ).all()

 if not reports:
 return {
 'region': region,
 'days': days,
 'report_count': 0,
 'drivers': [],
 'message': f'No reports found for {region} in the last {days} days'
 }

 # Extract and aggregate environmental features
 regional_data = self._aggregate_regional_data(reports)

 # Calculate hybrid risk scores for each feature
 risk_drivers = self._calculate_hybrid_scores(regional_data)

 # Get top drivers
 top_drivers = sorted(risk_drivers, key=lambda x: x['hybrid_score'], reverse=True)[:]

 # Add recommendations and icons
 for driver in top_drivers:
 driver['recommendation'] = self._get_recommendation(driver)
 driver['icon'] = self._get_icon(driver)

 return {
 'region': region,
 'days': days,
 'report_count': len(reports),
 'drivers': top_drivers,
 'metadata': {
 'analyzed_at': datetime.now().isoformat(),
 'total_features_analyzed': len(risk_drivers),
 'base_risk': self.bayesian_probs['metadata']['p_high_risk']
 }
 }

 except Exception as e:
 print(f" Error in get_regional_drivers: {e}")
 import traceback
 traceback.print_exc()
 return {
 'error': str(e),
 'drivers': [],
 'metadata': {}
 }

 def _aggregate_regional_data(self, reports: List) -> Dict:
 """
 Aggregate environmental features from reports

 Args:
 reports: List of Report objects

 Returns:
 Dictionary with aggregated feature values
 """
 aggregated = {}
 feature_values = {}

 for report in reports:
 try:
 # Parse water metrics
 water_metrics = json.loads(report.water_metrics)

 # Collect values for each feature
 for key, value in water_metrics.items():
 if value is not None and isinstance(value, (int, float)):
 if key not in feature_values:
 feature_values[key] = []
 feature_values[key].append(value)

 except (json.JSONDecodeError, AttributeError) as e:
 continue

 # Calculate averages
 for feature, values in feature_values.items():
 if values:
 aggregated[feature] = {
 'mean': np.mean(values),
 'median': np.median(values),
 'std': np.std(values),
 'min': np.min(values),
 'max': np.max(values),
 'count': len(values)
 }

 return aggregated

 def _calculate_hybrid_scores(self, regional_data: Dict) -> List[Dict]:
 """
 Calculate hybrid risk scores combining Bayesian probability,
 ML feature importance, and deviation from safe thresholds

 Args:
 regional_data: Aggregated regional feature data

 Returns:
 List of risk drivers with hybrid scores
 """
 risk_drivers = []

 thresholds = self.bayesian_probs.get('thresholds', {})
 cond_probs = self.bayesian_probs.get('conditional_probabilities', {})

 for feature, stats in regional_data.items():
 # Get current value (use mean)
 current_value = stats['mean']

 # Get Bayesian probability
 bayesian_score = self._get_bayesian_score(feature, current_value, cond_probs)

 # Get ML feature importance
 ml_importance = self._get_ml_importance(feature)

 # Get deviation from safe threshold
 deviation_score = self._get_deviation_score(feature, current_value, thresholds)

 # Calculate hybrid score (weighted combination)
 # Weights: Bayesian 0%, ML Importance 0%, Deviation 0%
 hybrid_score = (
 0. * bayesian_score +
 0. * ml_importance +
 0. * deviation_score
 )

 # Get safe threshold for comparison
 safe_value = self._get_safe_threshold(feature, thresholds)

 # Determine risk level
 risk_level = self._determine_risk_level(feature, current_value, thresholds)

 # Get threshold info for display
 threshold_info = thresholds.get(feature, {})
 unit = threshold_info.get('unit', '')

 # Format safe value display
 if 'max' in threshold_info:
 safe_value_display = f"<{threshold_info['max']} {unit}".strip()
 deviation_direction = 'above'
 elif 'min' in threshold_info:
 safe_value_display = f">{threshold_info['min']} {unit}".strip()
 deviation_direction = 'below'
 else:
 safe_value_display = safe_value
 deviation_direction = 'from'

 risk_drivers.append({
 # Basic info
 'feature': feature,
 'feature_display': get_friendly_name(feature),
 'factor': get_friendly_name(feature),
 'feature_key': feature,

 # Bayesian Probability (clearly labeled)
 'bayesian_probability': float(round(bayesian_score * 00, )), # e.g., .%
 'bayesian_label': f"P(High Risk | {get_friendly_name(feature)} elevated)",
 'bayesian_score': float(round(bayesian_score, )), # Keep original for compatibility

 # Model Feature Importance (clearly labeled)
 'model_importance': float(round(ml_importance * 00, )), # e.g., 0.%
 'model_label': "XGBoost Feature Weight",
 'ml_importance': float(round(ml_importance, )), # Keep original for compatibility

 # Combined/Hybrid Score (clearly labeled)
 'hybrid_score': float(round(hybrid_score, )),
 'hybrid_score_percentage': float(round(hybrid_score * 00, )), # e.g., .%
 'hybrid_label': "Combined Risk Driver Score",

 # Deviation Score
 'deviation_score': float(round(deviation_score, )),
 'deviation_percentage': float(round(deviation_score * 00, )), # e.g., .0%
 'deviation_direction': deviation_direction,

 # Values
 'current_value': float(round(current_value, )),
 'current_value_display': f"{round(current_value, )} {unit}".strip(),
 'safe_value': safe_value,
 'safe_value_display': safe_value_display,
 'deviation': f"{round(deviation_score * 00, )}% {deviation_direction} threshold",

 # Risk assessment
 'risk_level': risk_level,

 # Statistics
 'sample_count': int(stats['count']),
 'std_dev': float(round(stats['std'], )),

 # Recommendation and icon (will be added by main.py)
 'recommendation': '',
 'icon': ''
 })

 return risk_drivers

 def _get_bayesian_score(
 self,
 feature: str,
 value: float,
 cond_probs: Dict
 ) -> float:
 """Get Bayesian probability score (0-)"""
 if feature not in cond_probs:
 return 0.0

 # Determine risk level
 thresholds = self.bayesian_probs.get('thresholds', {})
 risk_level = self._determine_risk_level(feature, value, thresholds)

 # Get Bayesian probability for this risk level
 if risk_level in cond_probs[feature]:
 return cond_probs[feature][risk_level].get('p_high_risk_given_feature', 0.0)

 return 0.0

 def _get_ml_importance(self, feature: str) -> float:
 """Get normalized ML feature importance (0-)"""
 if self.feature_importance is None:
 return 0.0

 # Try exact match first
 match = self.feature_importance[self.feature_importance['feature'] == feature]

 if not match.empty:
 # Normalize to 0- range
 max_importance = self.feature_importance['importance'].max()
 return match.iloc[0]['importance'] / max_importance if max_importance > 0 else 0.0

 # Try partial match (for encoded features)
 partial_matches = self.feature_importance[
 self.feature_importance['feature'].str.contains(feature, case=False, na=False)
 ]

 if not partial_matches.empty:
 # Use average importance of matching features
 max_importance = self.feature_importance['importance'].max()
 avg_importance = partial_matches['importance'].mean()
 return avg_importance / max_importance if max_importance > 0 else 0.0

 return 0.0

 def _get_deviation_score(
 self,
 feature: str,
 value: float,
 thresholds: Dict
 ) -> float:
 """Calculate deviation from safe threshold (0-)"""
 if feature not in thresholds:
 return 0.0

 threshold = thresholds[feature]

 # Handle different threshold types
 if 'safe' in threshold and 'high_risk' in threshold:
 safe = threshold['safe']
 high_risk = threshold['high_risk']

 if value <= safe:
 return 0.0
 elif value >= high_risk:
 return .0
 else:
 # Linear interpolation between safe and high_risk
 return (value - safe) / (high_risk - safe)

 # Handle range-based thresholds (pH, temperature, humidity)
 elif 'safe_min' in threshold and 'safe_max' in threshold:
 safe_min = threshold['safe_min']
 safe_max = threshold['safe_max']

 if safe_min <= value <= safe_max:
 return 0.0
 else:
 # Calculate distance from safe range
 if value < safe_min:
 deviation = safe_min - value
 max_deviation = safe_min - threshold.get('elevated_min', safe_min - )
 else:
 deviation = value - safe_max
 max_deviation = threshold.get('elevated_max', safe_max + ) - safe_max

 return min(deviation / max_deviation, .0) if max_deviation > 0 else 0.0

 return 0.0

 def _determine_risk_level(
 self,
 feature: str,
 value: float,
 thresholds: Dict
 ) -> str:
 """Determine risk level (safe, elevated, high_risk)"""
 if feature not in thresholds:
 return 'unknown'

 threshold = thresholds[feature]

 # Handle standard thresholds
 if 'safe' in threshold and 'elevated' in threshold and 'high_risk' in threshold:
 if value <= threshold['safe']:
 return 'safe'
 elif value <= threshold['elevated']:
 return 'elevated'
 else:
 return 'high_risk'

 # Handle range-based thresholds
 elif 'safe_min' in threshold and 'safe_max' in threshold:
 if threshold['safe_min'] <= value <= threshold['safe_max']:
 return 'safe'
 elif threshold.get('elevated_min', 0) <= value <= threshold.get('elevated_max', 00):
 return 'elevated'
 else:
 return 'high_risk'

 return 'unknown'

 def _get_safe_threshold(self, feature: str, thresholds: Dict) -> Optional[float]:
 """Get safe threshold value for display"""
 if feature not in thresholds:
 return None

 threshold = thresholds[feature]

 if 'safe' in threshold:
 return float(threshold['safe'])
 elif 'safe_min' in threshold and 'safe_max' in threshold:
 # Return as string for range
 return f"{threshold['safe_min']}-{threshold['safe_max']}"

 return None

 def _get_recommendation(self, driver: Dict) -> str:
 """Generate actionable recommendation based on risk driver"""
 feature = driver['feature']
 risk_level = driver['risk_level']
 current = driver['current_value']
 safe = driver['safe_value']

 recommendations = {
 'fecal_coliform_per_00ml': {
 'high_risk': f"CRITICAL: Fecal coliform at {current:.0f} per 00ml (safe: {safe}). Immediate water treatment and source investigation required. Do not consume without boiling.",
 'elevated': f"WARNING: Elevated fecal coliform at {current:.0f} per 00ml. Implement water treatment and monitor source.",
 'safe': "Fecal coliform within safe limits. Continue monitoring."
 },
 'ph': {
 'high_risk': f"pH at {current:.f} is outside safe range ({safe}). Adjust water treatment process. Extreme pH can affect disinfection effectiveness.",
 'elevated': f"pH at {current:.f} is slightly outside optimal range. Monitor and adjust if needed.",
 'safe': "pH within safe range."
 },
 'turbidity_ntu': {
 'high_risk': f"High turbidity ({current:.f} NTU, safe: <{safe}). Improve filtration. High turbidity shields pathogens from disinfection.",
 'elevated': f"Elevated turbidity ({current:.f} NTU). Enhance filtration processes.",
 'safe': "Turbidity within acceptable limits."
 },
 'arsenic_ug_l': {
 'high_risk': f"CRITICAL: Arsenic at {current:.0f} μg/l exceeds safe limit ({safe}). Long-term exposure causes cancer. Install arsenic removal system immediately.",
 'elevated': f"Arsenic at {current:.0f} μg/l approaching unsafe levels. Consider arsenic removal treatment.",
 'safe': "Arsenic within safe limits."
 },
 'nitrate_mg_l': {
 'high_risk': f"High nitrate ({current:.f} mg/l, safe: <{safe}). Risk of methemoglobinemia in infants. Identify agricultural/sewage contamination source.",
 'elevated': f"Elevated nitrate ({current:.f} mg/l). Monitor for agricultural runoff.",
 'safe': "Nitrate within safe limits."
 }
 }

 # Get specific recommendation or generic one
 if feature in recommendations and risk_level in recommendations[feature]:
 return recommendations[feature][risk_level]

 # Generic recommendation
 if risk_level == 'high_risk':
 return f"High risk detected for {driver['feature_display']}. Immediate action required."
 elif risk_level == 'elevated':
 return f"Elevated {driver['feature_display']}. Enhanced monitoring recommended."
 else:
 return f"{driver['feature_display']} within acceptable range."

 def _get_icon(self, driver: Dict) -> str:
 """Get emoji icon based on risk level"""
 risk_level = driver['risk_level']

 icons = {
 'high_risk': '',
 'elevated': '',
 'safe': '',
 'unknown': ''
 }

 return icons.get(risk_level, '')

# Global instance
risk_analyzer: Optional[BayesianRiskAnalyzer] = None

def initialize_analyzer(models_dir: str = "./models") -> bool:
 """
 Initialize the global risk analyzer instance

 Args:
 models_dir: Directory containing model files

 Returns:
 True if initialization successful, False otherwise
 """
 global risk_analyzer

 try:
 risk_analyzer = BayesianRiskAnalyzer(models_dir=models_dir)
 return risk_analyzer.model is not None and risk_analyzer.bayesian_probs is not None
 except Exception as e:
 print(f" Failed to initialize risk analyzer: {e}")
 return False

def get_analyzer() -> Optional[BayesianRiskAnalyzer]:
 """Get the global risk analyzer instance"""
 return risk_analyzer

# Test function for standalone execution
def test_analyzer():
 """Test the risk analyzer with sample data"""
 print("\n" + "=" * 0)
 print(" TESTING BAYESIAN RISK ANALYZER")
 print("=" * 0)

 # Initialize analyzer
 success = initialize_analyzer()

 if not success:
 print(" Failed to initialize analyzer")
 return

 print("\n Analyzer initialized successfully")
 print(f" Model loaded: {risk_analyzer.model is not None}")
 print(f" Bayesian probs loaded: {risk_analyzer.bayesian_probs is not None}")
 print(f" Feature importance available: {risk_analyzer.feature_importance is not None}")

 if risk_analyzer.feature_importance is not None:
 print(f"\n Top ML Features by Importance:")
 for i, row in risk_analyzer.feature_importance.head().iterrows():
 print(f" {i+}. {row['feature']}: {row['importance']:.f}")

 if risk_analyzer.bayesian_probs:
 print(f"\n Bayesian Probabilities:")
 print(f" Base risk: {risk_analyzer.bayesian_probs['metadata']['p_high_risk']:.%}")
 print(f" Features analyzed: {len(risk_analyzer.bayesian_probs['conditional_probabilities'])}")

 print("\n" + "=" * 0)
 print(" Test complete!")
 print("=" * 0)

if __name__ == "__main__":
 test_analyzer()
