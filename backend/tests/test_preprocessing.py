"""
Test preprocessing logic standalone
"""
import joblib
import pandas as pd

print("=" * 80)
print("TESTING PREPROCESSING LOGIC")
print("=" * 80)

# Load artifacts
print("\n[1/4] Loading artifacts...")
model = joblib.load('./models/best_model.pkl')
scaler = joblib.load('./models/scaler.pkl')
label_encoder = joblib.load('./models/label_encoder.pkl')
feature_names = joblib.load('./models/feature_names.pkl')
preprocessing_info = joblib.load('./models/preprocessing_info.pkl')
print(f"✅ Loaded: {len(feature_names)} features")

# Create sample data
print("\n[2/4] Creating sample data...")
input_data = {
    'district': 'Test_District',
    'is_urban': 1,
    'population_density': 5000,
    'age': 35,
    'gender': 'Male',
    'water_source': 'Tap',
    'water_treatment': 'Chlorination',
    'water_quality_index': 45.0,
    'ph': 6.8,
    'turbidity_ntu': 8.0,
    'dissolved_oxygen_mg_l': 7.5,
    'bod_mg_l': 4.0,
    'fecal_coliform_per_100ml': 150,
    'total_coliform_per_100ml': 300,
    'tds_mg_l': 400.0,
    'nitrate_mg_l': 8.0,
    'fluoride_mg_l': 0.7,
    'arsenic_ug_l': 8.0,
    'open_defecation_rate': 0.05,
    'toilet_access': 1,
    'sewage_treatment_pct': 75.0,
    'handwashing_practice': 'Always',
    'month': 6,
    'season': 'Summer',
    'avg_temperature_c': 28.0,
    'avg_rainfall_mm': 150.0,
    'avg_humidity_pct': 65.0,
    'flooding': 0,
    'symptom_diarrhea': 1,
    'symptom_vomiting': 1,
    'symptom_fever': 1,
    'symptom_abdominal_pain': 1,
    'symptom_dehydration': 0,
    'symptom_jaundice': 0,
    'symptom_bloody_stool': 0,
    'symptom_skin_rash': 0
}

df = pd.DataFrame([input_data])
print(f"✅ Created DataFrame: {df.shape}")

# Preprocess
print("\n[3/4] Preprocessing...")

# Label encode district and handwashing_practice
if 'district' in df.columns and df['district'].dtype == 'object':
    df['district'] = df['district'].apply(lambda x: hash(str(x)) % 1000)
    print(f"✅ Label encoded district: {df['district'].values[0]}")

if 'handwashing_practice' in df.columns and df['handwashing_practice'].dtype == 'object':
    handwashing_map = {'Always': 2, 'Sometimes': 1, 'Rarely': 0, 'Never': 0}
    df['handwashing_practice'] = df['handwashing_practice'].map(handwashing_map).fillna(1)
    print(f"✅ Label encoded handwashing: {df['handwashing_practice'].values[0]}")

# One-hot encode
onehot_cols = preprocessing_info.get('onehot_cols', [])
print(f"✅ One-hot encoding: {onehot_cols}")
df_encoded = pd.get_dummies(df, columns=onehot_cols, drop_first=True)
print(f"✅ After encoding: {df_encoded.shape}")

# Add missing columns
for col in feature_names:
    if col not in df_encoded.columns:
        df_encoded[col] = 0

# Reorder
df_encoded = df_encoded.reindex(columns=feature_names, fill_value=0)
print(f"✅ After reordering: {df_encoded.shape}")

# Scale
df_scaled = scaler.transform(df_encoded)
print(f"✅ After scaling: {df_scaled.shape}")

# Predict
print("\n[4/4] Making prediction...")
prediction = model.predict(df_scaled)[0]
prediction_proba = model.predict_proba(df_scaled)[0]
predicted_disease = label_encoder.inverse_transform([prediction])[0]
confidence = prediction_proba.max()

print(f"✅ Predicted disease: {predicted_disease}")
print(f"✅ Confidence: {confidence:.2%}")
print(f"✅ Prediction class: {prediction}")

print("\n" + "=" * 80)
print("✅ PREPROCESSING TEST SUCCESSFUL!")
print("=" * 80)
