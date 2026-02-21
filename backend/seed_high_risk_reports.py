"""
Seed script to create 10 high-risk reports for Coimbatore North
This will trigger ML predictions and potentially create alerts
"""
import sys
import json
from datetime import datetime
from database import SessionLocal, engine
import models
import joblib
import pandas as pd
import numpy as np

# Load ML models
print("=" * 80)
print("LOADING ML MODELS...")
print("=" * 80)

try:
    model = joblib.load('./models/best_model.pkl')
    scaler = joblib.load('./models/scaler.pkl')
    label_encoder = joblib.load('./models/label_encoder.pkl')
    feature_names = joblib.load('./models/feature_names.pkl')
    preprocessing_info = joblib.load('./models/preprocessing_info.pkl')
    print(" ML models loaded successfully")
except Exception as e:
    print(f" Error loading models: {e}")
    sys.exit(1)

def preprocess_and_predict(report_data):
    """Preprocess data and make prediction"""
    # Create input data dictionary
    input_data = {
        'district': hash(report_data['district']) % 1000,
        'is_urban': int(report_data['is_urban']),
        'population_density': report_data['population_density'],
        'age': report_data['age'],
        'gender': report_data['gender'],
        'water_source': report_data['water_source'],
        'water_treatment': report_data['water_treatment'],
        'water_quality_index': report_data['water_metrics']['water_quality_index'],
        'ph': report_data['water_metrics']['ph'],
        'turbidity_ntu': report_data['water_metrics']['turbidity_ntu'],
        'dissolved_oxygen_mg_l': report_data['water_metrics']['dissolved_oxygen_mg_l'],
        'bod_mg_l': report_data['water_metrics']['bod_mg_l'],
        'fecal_coliform_per_100ml': report_data['water_metrics']['fecal_coliform_per_100ml'],
        'total_coliform_per_100ml': report_data['water_metrics']['total_coliform_per_100ml'],
        'tds_mg_l': report_data['water_metrics']['tds_mg_l'],
        'nitrate_mg_l': report_data['water_metrics']['nitrate_mg_l'],
        'fluoride_mg_l': report_data['water_metrics']['fluoride_mg_l'],
        'arsenic_ug_l': report_data['water_metrics']['arsenic_ug_l'],
        'open_defecation_rate': report_data['open_defecation_rate'],
        'toilet_access': report_data['toilet_access'],
        'sewage_treatment_pct': report_data['sewage_treatment_pct'],
        'handwashing_practice': 0,  # Rarely
        'month': report_data['month'],
        'season': report_data['season'],
        'avg_temperature_c': report_data['avg_temperature_c'],
        'avg_rainfall_mm': report_data['avg_rainfall_mm'],
        'avg_humidity_pct': report_data['avg_humidity_pct'],
        'flooding': int(report_data['flooding']),
        'symptom_diarrhea': int(report_data['symptoms']['diarrhea']),
        'symptom_vomiting': int(report_data['symptoms']['vomiting']),
        'symptom_fever': int(report_data['symptoms']['fever']),
        'symptom_abdominal_pain': int(report_data['symptoms']['abdominal_pain']),
        'symptom_dehydration': int(report_data['symptoms']['dehydration']),
        'symptom_jaundice': int(report_data['symptoms']['jaundice']),
        'symptom_bloody_stool': int(report_data['symptoms']['bloody_stool']),
        'symptom_skin_rash': int(report_data['symptoms']['skin_rash'])
    }
    
    # Convert to DataFrame
    df = pd.DataFrame([input_data])
    
    # One-hot encode categorical features
    onehot_cols = preprocessing_info.get('onehot_cols', [])
    if onehot_cols:
        df_encoded = pd.get_dummies(df, columns=onehot_cols, drop_first=True)
    else:
        df_encoded = df.copy()
    
    # Handle missing columns
    for col in feature_names:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    
    # Reorder columns
    df_encoded = df_encoded.reindex(columns=feature_names, fill_value=0)
    
    # Scale features
    df_scaled = scaler.transform(df_encoded)
    
    # Make prediction
    prediction_proba = model.predict_proba(df_scaled)[0]
    prediction_class = model.predict(df_scaled)[0]
    
    # Get disease name and confidence
    predicted_disease = label_encoder.inverse_transform([prediction_class])[0]
    confidence = float(np.max(prediction_proba))
    
    # Calculate risk score
    risk_score = confidence if predicted_disease != "No_Disease" else 1 - confidence
    
    # Determine risk level
    if risk_score >= 0.6:
        risk_level = "High"
    elif risk_score >= 0.3:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    return {
        'predicted_disease': predicted_disease,
        'confidence': confidence,
        'risk_score': risk_score * 100,
        'risk_level': risk_level
    }

def create_high_risk_reports():
    """Create 10 high-risk reports for Coimbatore North"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 80)
        print("CREATING 10 HIGH-RISK REPORTS FOR COIMBATORE NORTH")
        print("=" * 80 + "\n")
        
        # Get or create a test user
        user = db.query(models.User).filter(models.User.email == "community@example.com").first()
        if not user:
            print(" Test user not found. Please run create_demo_users.py first.")
            return
        
        reports_created = 0
        predictions_created = 0
        high_risk_count = 0
        
        for i in range(1, 11):
            # High-risk report data
            report_data = {
                'region': 'Coimbatore South',
                'district': 'Coimbatore',
                'is_urban': True,
                'population_density': 5000,
                'age': 25 + (i * 3),  # Vary age
                'gender': 'Male' if i % 2 == 0 else 'Female',
                'water_source': 'River',
                'water_treatment': 'None',
                'open_defecation_rate': 0.6,
                'toilet_access': 0,
                'sewage_treatment_pct': 10.0,
                'month': datetime.now().month,
                'season': 'Monsoon',
                'avg_temperature_c': 32.0,
                'avg_rainfall_mm': 250.0,
                'avg_humidity_pct': 85.0,
                'flooding': True,
                'symptoms': {
                    'diarrhea': True,
                    'vomiting': True,
                    'fever': True,
                    'abdominal_pain': True,
                    'dehydration': True,
                    'jaundice': False,
                    'bloody_stool': True,
                    'skin_rash': False
                },
                'water_metrics': {
                    'water_quality_index': 10.0,  # Very poor quality
                    'ph': 5.5,  # Acidic
                    'turbidity_ntu': 30.0,  # Very turbid
                    'dissolved_oxygen_mg_l': 2.0,  # Low oxygen
                    'bod_mg_l': 15.0,  # High BOD
                    'fecal_coliform_per_100ml': 5000 + (i * 200),  # Very high contamination
                    'total_coliform_per_100ml': 8000 + (i * 200),  # Very high
                    'tds_mg_l': 1200.0,  # High TDS
                    'nitrate_mg_l': 30.0,  # High nitrate
                    'fluoride_mg_l': 3.0,  # High fluoride
                    'arsenic_ug_l': 40.0  # High arsenic
                }
            }
            
            # Create report
            symptoms_json = json.dumps(report_data['symptoms'])
            water_metrics_json = json.dumps(report_data['water_metrics'])
            
            db_report = models.Report(
                user_id=user.id,
                region=report_data['region'],
                symptoms=symptoms_json,
                water_metrics=water_metrics_json
            )
            
            db.add(db_report)
            db.commit()
            db.refresh(db_report)
            reports_created += 1
            
            # Make prediction
            prediction = preprocess_and_predict(report_data)
            
            # Save prediction
            db_prediction = models.Prediction(
                region=report_data['region'],
                risk_score=prediction['risk_score'],
                risk_level=prediction['risk_level'],
                predicted_disease=prediction['predicted_disease'],
                confidence=prediction['confidence']
            )
            
            db.add(db_prediction)
            db.commit()
            db.refresh(db_prediction)
            predictions_created += 1
            
            if prediction['risk_level'] == 'High':
                high_risk_count += 1
            
            print(f" Report #{i}: Disease={prediction['predicted_disease']}, "
                  f"Risk={prediction['risk_level']} ({prediction['risk_score']:.1f}%), "
                  f"Confidence={prediction['confidence']:.2%}")
        
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f" Reports created: {reports_created}")
        print(f" Predictions created: {predictions_created}")
        print(f" High-risk predictions: {high_risk_count}")
        print(f" Region: Coimbatore North")
        print(f"\n TIP: Check the Admin Dashboard to see:")
        print(f"   - Regional risk map (should show Coimbatore North in red)")
        print(f"   - Alerts (if 5+ high-risk reports, alert should be created)")
        print(f"   - Weekly summary (should show 10 new reports)")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f" Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_high_risk_reports()
