"""
Test preprocessing logic standalone
"""
import joblib
import pandas as pd

print("=" * 0)
print("TESTING PREPROCESSING LOGIC")
print("=" * 0)

# Load artifacts
print("\n[/] Loading artifacts...")
model = joblib.load('./models/best_model.pkl')
scaler = joblib.load('./models/scaler.pkl')
label_encoder = joblib.load('./models/label_encoder.pkl')
feature_names = joblib.load('./models/feature_names.pkl')
preprocessing_info = joblib.load('./models/preprocessing_info.pkl')
print(f" Loaded: {len(feature_names)} features")

# Create sample data
print("\n[/] Creating sample data...")
input_data = {
 'district': 'Test_District',
 'is_urban': ,
 'population_density': 000,
 'age': ,
 'gender': 'Male',
 'water_source': 'Tap',
 'water_treatment': 'Chlorination',
 'water_quality_index': .0,
 'ph': .,
 'turbidity_ntu': .0,
 'dissolved_oxygen_mg_l': .,
 'bod_mg_l': .0,
 'fecal_coliform_per_00ml': 0,
 'total_coliform_per_00ml': 00,
 'tds_mg_l': 00.0,
 'nitrate_mg_l': .0,
 'fluoride_mg_l': 0.,
 'arsenic_ug_l': .0,
 'open_defecation_rate': 0.0,
 'toilet_access': ,
 'sewage_treatment_pct': .0,
 'handwashing_practice': 'Always',
 'month': ,
 'season': 'Summer',
 'avg_temperature_c': .0,
 'avg_rainfall_mm': 0.0,
 'avg_humidity_pct': .0,
 'flooding': 0,
 'symptom_diarrhea': ,
 'symptom_vomiting': ,
 'symptom_fever': ,
 'symptom_abdominal_pain': ,
 'symptom_dehydration': 0,
 'symptom_jaundice': 0,
 'symptom_bloody_stool': 0,
 'symptom_skin_rash': 0
}

df = pd.DataFrame([input_data])
print(f" Created DataFrame: {df.shape}")

# Preprocess
print("\n[/] Preprocessing...")

# Label encode district and handwashing_practice
if 'district' in df.columns and df['district'].dtype == 'object':
 df['district'] = df['district'].apply(lambda x: hash(str(x)) % 000)
 print(f" Label encoded district: {df['district'].values[0]}")

if 'handwashing_practice' in df.columns and df['handwashing_practice'].dtype == 'object':
 handwashing_map = {'Always': , 'Sometimes': , 'Rarely': 0, 'Never': 0}
 df['handwashing_practice'] = df['handwashing_practice'].map(handwashing_map).fillna()
 print(f" Label encoded handwashing: {df['handwashing_practice'].values[0]}")

# One-hot encode
onehot_cols = preprocessing_info.get('onehot_cols', [])
print(f" One-hot encoding: {onehot_cols}")
df_encoded = pd.get_dummies(df, columns=onehot_cols, drop_first=True)
print(f" After encoding: {df_encoded.shape}")

# Add missing columns
for col in feature_names:
 if col not in df_encoded.columns:
 df_encoded[col] = 0

# Reorder
df_encoded = df_encoded.reindex(columns=feature_names, fill_value=0)
print(f" After reordering: {df_encoded.shape}")

# Scale
df_scaled = scaler.transform(df_encoded)
print(f" After scaling: {df_scaled.shape}")

# Predict
print("\n[/] Making prediction...")
prediction = model.predict(df_scaled)[0]
prediction_proba = model.predict_proba(df_scaled)[0]
predicted_disease = label_encoder.inverse_transform([prediction])[0]
confidence = prediction_proba.max()

print(f" Predicted disease: {predicted_disease}")
print(f" Confidence: {confidence:.%}")
print(f" Prediction class: {prediction}")

print("\n" + "=" * 0)
print(" PREPROCESSING TEST SUCCESSFUL!")
print("=" * 0)
