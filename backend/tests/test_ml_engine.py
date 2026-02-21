"""
Test script for ML Engine regional risk analysis
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from ml_engine import initialize_analyzer, get_analyzer
from database import get_db
import models

def test_regional_drivers():
    """Test the get_regional_drivers function"""
    print("=" * 80)
    print("🧪 TESTING REGIONAL RISK DRIVERS ANALYSIS")
    print("=" * 80)
    
    # Initialize analyzer
    print("\n📂 Initializing analyzer...")
    success = initialize_analyzer()
    
    if not success:
        print("❌ Failed to initialize analyzer")
        return
    
    analyzer = get_analyzer()
    print("✅ Analyzer initialized")
    
    # Get database session
    db = next(get_db())
    
    # Test with different regions
    test_regions = [
        ("Coimbatore North", 7),
        ("TestRegion", 7),
        ("Chennai", 30)
    ]
    
    for region, days in test_regions:
        print("\n" + "=" * 80)
        print(f"📍 Analyzing: {region} (Last {days} days)")
        print("=" * 80)
        
        result = analyzer.get_regional_drivers(db, region, days)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            continue
        
        if result['report_count'] == 0:
            print(f"⚠️  {result.get('message', 'No data available')}")
            continue
        
        print(f"\n📊 Analysis Results:")
        print(f"   Region: {result['region']}")
        print(f"   Reports analyzed: {result['report_count']}")
        print(f"   Time period: {result['days']} days")
        print(f"   Features analyzed: {result['metadata']['total_features_analyzed']}")
        print(f"   Base risk: {result['metadata']['base_risk']:.2%}")
        
        if result['drivers']:
            print(f"\n🔴 Top {len(result['drivers'])} Risk Drivers:")
            
            for i, driver in enumerate(result['drivers'], 1):
                print(f"\n   {i}. {driver['icon']} {driver['feature_display']}")
                print(f"      Current: {driver['current_value']}")
                print(f"      Safe: {driver['safe_value']}")
                print(f"      Risk Level: {driver['risk_level'].upper()}")
                print(f"      Hybrid Score: {driver['hybrid_score']:.4f}")
                print(f"      ├─ Bayesian: {driver['bayesian_score']:.4f}")
                print(f"      ├─ ML Importance: {driver['ml_importance']:.4f}")
                print(f"      └─ Deviation: {driver['deviation_score']:.4f}")
                print(f"      Samples: {driver['sample_count']}")
                print(f"      Recommendation: {driver['recommendation']}")
        else:
            print("\n✅ No significant risk drivers detected")
    
    print("\n" + "=" * 80)
    print("✅ Regional risk analysis test complete!")
    print("=" * 80)

def test_feature_scoring():
    """Test individual feature scoring components"""
    print("\n" + "=" * 80)
    print("🧪 TESTING FEATURE SCORING COMPONENTS")
    print("=" * 80)
    
    analyzer = get_analyzer()
    if not analyzer:
        print("❌ Analyzer not initialized")
        return
    
    # Test features with known values
    test_cases = [
        ('fecal_coliform_per_100ml', 3000),
        ('ph', 6.2),
        ('turbidity_ntu', 15),
        ('arsenic_ug_l', 120),
        ('nitrate_mg_l', 55)
    ]
    
    print("\n📊 Feature Scoring Breakdown:")
    
    for feature, value in test_cases:
        print(f"\n{feature} = {value}")
        
        # Get Bayesian score
        cond_probs = analyzer.bayesian_probs.get('conditional_probabilities', {})
        bayesian_score = analyzer._get_bayesian_score(feature, value, cond_probs)
        
        # Get ML importance
        ml_importance = analyzer._get_ml_importance(feature)
        
        # Get deviation score
        thresholds = analyzer.bayesian_probs.get('thresholds', {})
        deviation_score = analyzer._get_deviation_score(feature, value, thresholds)
        
        # Calculate hybrid
        hybrid_score = 0.4 * bayesian_score + 0.3 * ml_importance + 0.3 * deviation_score
        
        print(f"  Bayesian Score: {bayesian_score:.4f} (40% weight)")
        print(f"  ML Importance: {ml_importance:.4f} (30% weight)")
        print(f"  Deviation Score: {deviation_score:.4f} (30% weight)")
        print(f"  → Hybrid Score: {hybrid_score:.4f}")
    
    print("\n" + "=" * 80)
    print("✅ Feature scoring test complete!")
    print("=" * 80)

def main():
    """Run all tests"""
    # Test regional drivers
    test_regional_drivers()
    
    # Test feature scoring
    test_feature_scoring()

if __name__ == "__main__":
    main()
