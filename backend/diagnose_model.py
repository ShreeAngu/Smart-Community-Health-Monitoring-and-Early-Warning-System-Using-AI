"""
Diagnostic script to check ML model loading and preprocessing
"""
import joblib
import pandas as pd
import os

print("=" * 80)
print("ML MODEL DIAGNOSTICS")
print("=" * 80)

# Check if files exist
print("\n[1/5] Checking model files...")
model_files = {
    'best_model.pkl': './models/best_model.pkl',
    'scaler.pkl': './models/scaler.pkl',
    'label_encoder.pkl': './models/label_encoder.pkl',
    'feature_names.pkl': './models/feature_names.pkl',
    'preprocessing_info.pkl': './models/preprocessing_info.pkl'
}

for name, path in model_files.items():
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {name}: {path}")

# Load artifacts
print("\n[2/5] Loading artifacts...")
try:
    model = joblib.load('./models/best_model.pkl')
    print(f"✅ Model type: {type(model).__name__}")
    
    scaler = joblib.load('./models/scaler.pkl')
    print(f"✅ Scaler type: {type(scaler).__name__}")
    
    label_encoder = joblib.load('./models/label_encoder.pkl')
    print(f"✅ Label encoder classes: {label_encoder.classes_}")
    
    feature_names = joblib.load('./models/feature_names.pkl')
    print(f"✅ Feature names count: {len(feature_names)}")
    
    preprocessing_info = joblib.load('./models/preprocessing_info.pkl')
    print(f"✅ Preprocessing info keys: {preprocessing_info.keys()}")
    
except Exception as e:
    print(f"❌ Error loading: {e}")
    exit(1)

# Check preprocessing info
print("\n[3/5] Preprocessing configuration...")
print(f"One-hot columns: {preprocessing_info.get('onehot_cols', [])}")
print(f"Exclude columns: {preprocessing_info.get('exclude_cols', [])}")
print(f"Best model: {preprocessing_info.get('best_model_name', 'Unknown')}")

# Show first 10 feature names
print("\n[4/5] First 10 feature names:")
for i, fname in enumerate(feature_names[:10], 1):
    print(f"  {i}. {fname}")

print("\n" + "=" * 80)
print("DIAGNOSTICS COMPLETE")
print("=" * 80)
