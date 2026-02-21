from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta
import json
import joblib
import pandas as pd
import numpy as np
from typing import List, Dict, Any

# Import local modules
from database import engine, get_db
import models
import schemas
import auth
from utils.csv_sync import append_report_to_csv
from ml_engine import initialize_analyzer, get_analyzer

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Water-Borne Disease Prediction API",
    description="API for predicting water-borne diseases based on water quality and symptoms",
    version="1.0.0"
)

# Add CORS middleware - Enable frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative React dev server
        "*"  # Allow all for development (configure appropriately for production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for ML artifacts
model = None
scaler = None
label_encoder = None
feature_names = None
preprocessing_info = None
feature_importance_data = None

# Alert system thresholds
ALERT_THRESHOLDS = {
    "AI_RISK_SCORE": 65,      # 65% average risk score
    "VOLUME_CASES": 9,         # 9 cases in rolling window
    "VOLUME_DAYS": 7,          # 7-day rolling window
    "COOLDOWN_HOURS": 24       # 24-hour cooldown between alerts
}

@app.on_event("startup")
async def load_ml_models():
    """Load ML model and preprocessors on startup"""
    global model, scaler, label_encoder, feature_names, preprocessing_info, feature_importance_data
    
    try:
        print("=" * 80)
        print("🚀 Loading ML models...")
        print("=" * 80)
        
        model_path = './models/best_model.pkl'
        scaler_path = './models/scaler.pkl'
        encoder_path = './models/label_encoder.pkl'
        features_path = './models/feature_names.pkl'
        preprocessing_path = './models/preprocessing_info.pkl'
        
        # Check if all required files exist
        import os
        missing_files = []
        for path in [model_path, scaler_path, encoder_path, features_path, preprocessing_path]:
            if not os.path.exists(path):
                missing_files.append(path)
        
        if missing_files:
            print("❌ ERROR: Missing ML model files:")
            for file in missing_files:
                print(f"   - {file}")
            print("\n⚠️  Server will start but ML predictions will be unavailable.")
            print("   Run 'python train_model.py' to generate model files.\n")
            model = None
            scaler = None
            label_encoder = None
            feature_names = None
            preprocessing_info = None
            feature_importance_data = None
            return
        
        # Load all artifacts
        model = joblib.load(model_path)
        print(f"✅ Model loaded: {model_path}")
        
        scaler = joblib.load(scaler_path)
        print(f"✅ Scaler loaded: {scaler_path}")
        
        label_encoder = joblib.load(encoder_path)
        print(f"✅ Label encoder loaded: {encoder_path}")
        
        feature_names = joblib.load(features_path)
        print(f"✅ Feature names loaded: {len(feature_names)} features")
        
        preprocessing_info = joblib.load(preprocessing_path)
        print(f"✅ Preprocessing info loaded")
        
        # Get feature importances for the feature importance endpoint
        if hasattr(model, 'feature_importances_'):
            feature_importance_data = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            print(f"✅ Feature importance data prepared")
        else:
            feature_importance_data = None
            print("⚠️  Model does not have feature_importances_ attribute")
        
        print("=" * 80)
        print("✅ ML models loaded successfully!")
        print("=" * 80)
        
        # Initialize Bayesian Risk Analyzer
        print("\n🔬 Initializing Bayesian Risk Analyzer...")
        analyzer_success = initialize_analyzer(models_dir="./models")
        if analyzer_success:
            print("✅ Bayesian Risk Analyzer initialized successfully!")
        else:
            print("⚠️  Bayesian Risk Analyzer initialization failed")
            print("   Regional risk driver analysis will be unavailable")
        
    except Exception as e:
        print("=" * 80)
        print(f"❌ ERROR loading ML models: {e}")
        print("=" * 80)
        print("⚠️  Server will start but ML predictions will be unavailable.")
        print("   Check that model files exist in ./models/ directory.\n")
        model = None
        scaler = None
        label_encoder = None
        feature_names = None
        preprocessing_info = None
        feature_importance_data = None

def predict_disease_probabilities(processed_data: pd.DataFrame) -> Dict:
    """
    Make ML prediction and return all class probabilities
    
    Args:
        processed_data: Preprocessed DataFrame ready for model input
        
    Returns:
        Dict containing predicted_disease, confidence, and all_class_probabilities
    """
    if model is None or label_encoder is None:
        raise HTTPException(status_code=503, detail="ML model not available")
    
    try:
        # Get probability distribution for all classes
        prediction_proba = model.predict_proba(processed_data)[0]
        
        # Get class names from label encoder
        class_names = label_encoder.classes_
        
        # Create list of all probabilities sorted by probability (descending)
        all_probs = [
            {"disease": name, "probability": float(prob)}
            for name, prob in zip(class_names, prediction_proba)
        ]
        all_probs.sort(key=lambda x: x["probability"], reverse=True)
        
        # Top prediction
        predicted_disease = all_probs[0]["disease"]
        confidence = all_probs[0]["probability"]
        
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
            "predicted_disease": predicted_disease,
            "confidence": confidence,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "all_class_probabilities": all_probs
        }
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Disease prediction failed: {str(e)}"
        )

def preprocess_input_data(report_data: schemas.ReportSubmit) -> pd.DataFrame:
    """Preprocess input data for model prediction"""
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="ML model not available")
    
    # Create input data dictionary matching training features
    input_data = {
        'district': report_data.district or 'Unknown',
        'is_urban': int(report_data.is_urban) if report_data.is_urban is not None else 0,
        'population_density': report_data.population_density or 1000,
        'age': report_data.age or 30,
        'gender': report_data.gender or 'Male',
        'water_source': report_data.water_source or 'Tap',
        'water_treatment': report_data.water_treatment or 'None',
        'water_quality_index': report_data.water_metrics.water_quality_index or 50.0,
        'ph': report_data.water_metrics.ph or 7.0,
        'turbidity_ntu': report_data.water_metrics.turbidity_ntu or 5.0,
        'dissolved_oxygen_mg_l': report_data.water_metrics.dissolved_oxygen_mg_l or 8.0,
        'bod_mg_l': report_data.water_metrics.bod_mg_l or 3.0,
        'fecal_coliform_per_100ml': report_data.water_metrics.fecal_coliform_per_100ml or 0,
        'total_coliform_per_100ml': report_data.water_metrics.total_coliform_per_100ml or 0,
        'tds_mg_l': report_data.water_metrics.tds_mg_l or 300.0,
        'nitrate_mg_l': report_data.water_metrics.nitrate_mg_l or 5.0,
        'fluoride_mg_l': report_data.water_metrics.fluoride_mg_l or 0.5,
        'arsenic_ug_l': report_data.water_metrics.arsenic_ug_l or 5.0,
        'open_defecation_rate': report_data.open_defecation_rate or 0.1,
        'toilet_access': report_data.toilet_access or 1,
        'sewage_treatment_pct': report_data.sewage_treatment_pct or 50.0,
        'handwashing_practice': report_data.handwashing_practice or 'Sometimes',
        'month': report_data.month or 6,
        'season': report_data.season or 'Summer',
        'avg_temperature_c': report_data.avg_temperature_c or 25.0,
        'avg_rainfall_mm': report_data.avg_rainfall_mm or 100.0,
        'avg_humidity_pct': report_data.avg_humidity_pct or 60.0,
        'flooding': int(report_data.flooding) if report_data.flooding is not None else 0,
        'symptom_diarrhea': int(report_data.symptoms.diarrhea),
        'symptom_vomiting': int(report_data.symptoms.vomiting),
        'symptom_fever': int(report_data.symptoms.fever),
        'symptom_abdominal_pain': int(report_data.symptoms.abdominal_pain),
        'symptom_dehydration': int(report_data.symptoms.dehydration),
        'symptom_jaundice': int(report_data.symptoms.jaundice),
        'symptom_bloody_stool': int(report_data.symptoms.bloody_stool),
        'symptom_skin_rash': int(report_data.symptoms.skin_rash)
    }
    
    # Convert to DataFrame
    df = pd.DataFrame([input_data])
    
    # Label encode district and handwashing_practice (they are numeric in training)
    # Use simple hash-based encoding for consistency
    if 'district' in df.columns and df['district'].dtype == 'object':
        df['district'] = df['district'].apply(lambda x: hash(str(x)) % 1000)
    
    if 'handwashing_practice' in df.columns and df['handwashing_practice'].dtype == 'object':
        # Map to numeric: Always=2, Sometimes=1, Rarely=0
        handwashing_map = {'Always': 2, 'Sometimes': 1, 'Rarely': 0, 'Never': 0}
        df['handwashing_practice'] = df['handwashing_practice'].map(handwashing_map).fillna(1)
    
    # One-hot encode categorical features (water_source, season, water_treatment, gender)
    onehot_cols = preprocessing_info.get('onehot_cols', [])
    if onehot_cols:
        df_encoded = pd.get_dummies(df, columns=onehot_cols, drop_first=True)
    else:
        df_encoded = df.copy()
    
    # Handle any missing columns that were in training
    for col in feature_names:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    
    # Reorder columns to match training
    df_encoded = df_encoded.reindex(columns=feature_names, fill_value=0)
    
    # Scale features
    df_scaled = scaler.transform(df_encoded)
    
    return pd.DataFrame(df_scaled, columns=feature_names)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Water-Borne Disease Prediction API",
        "version": "1.0.0",
        "status": "active",
        "ml_model_loaded": model is not None
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ml_model": "loaded" if model else "not_loaded",
        "model_details": {
            "model_type": type(model).__name__ if model else None,
            "scaler_loaded": scaler is not None,
            "label_encoder_loaded": label_encoder is not None,
            "feature_count": len(feature_names) if feature_names else 0,
            "preprocessing_info_loaded": preprocessing_info is not None
        }
    }

# Authentication endpoints
@app.post("/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/login", response_model=schemas.Token)
async def login(user_credentials: schemas.Login, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    user = auth.authenticate_user(user_credentials.email, user_credentials.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=schemas.UserResponse)
async def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    """Get current user information"""
    return current_user

# Report submission endpoint
@app.post("/submit-report", response_model=Dict[str, Any])
async def submit_report(
    report: schemas.ReportSubmit,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Accept symptom and water data, save to Reports table, and trigger prediction"""
    try:
        # Convert Pydantic models to JSON strings
        symptoms_json = json.dumps(report.symptoms.dict())
        water_metrics_json = json.dumps(report.water_metrics.dict())
        
        # Create report record
        db_report = models.Report(
            user_id=current_user.id,
            region=report.region,
            symptoms=symptoms_json,
            water_metrics=water_metrics_json
        )
        
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        print(f"✅ Report saved: ID={db_report.id}, Region={report.region}, User={current_user.email}")
        
        # Trigger prediction
        prediction_result = None
        db_prediction = None
        
        if model is not None:
            try:
                # Preprocess input data
                processed_data = preprocess_input_data(report)
                
                # Get full prediction with all class probabilities
                full_prediction = predict_disease_probabilities(processed_data)
                
                # Save prediction to database
                db_prediction = models.Prediction(
                    region=report.region,
                    risk_score=full_prediction["risk_score"] * 100,  # Convert to 0-100 scale for storage
                    risk_level=full_prediction["risk_level"],
                    predicted_disease=full_prediction["predicted_disease"],
                    confidence=full_prediction["confidence"]
                )
                
                db.add(db_prediction)
                db.commit()
                db.refresh(db_prediction)
                print(f"✅ Prediction saved: ID={db_prediction.id}, Disease={full_prediction['predicted_disease']}, Risk={full_prediction['risk_level']}")
                
                prediction_result = {
                    "prediction_id": db_prediction.id,
                    "predicted_disease": full_prediction["predicted_disease"],
                    "risk_score": full_prediction["risk_score"],
                    "risk_level": full_prediction["risk_level"],
                    "confidence": full_prediction["confidence"],
                    "all_class_probabilities": full_prediction["all_class_probabilities"]
                }
                
                # Sync to CSV for continuous learning
                try:
                    report_dict = report.dict()
                    csv_sync_success = append_report_to_csv(report_dict, prediction_result)
                    if csv_sync_success:
                        print(f"✅ CSV sync completed for report ID={db_report.id}")
                    else:
                        print(f"⚠️  CSV sync failed for report ID={db_report.id}")
                except Exception as csv_error:
                    print(f"⚠️  CSV sync error: {csv_error}")
                    # Don't fail the request if CSV sync fails
                
                # Check for auto-alerts after successful prediction
                try:
                    await check_auto_alerts(report.region, db)
                except Exception as alert_error:
                    print(f"⚠️  Alert check error: {alert_error}")
                    # Don't fail the request if alert checking fails
                
            except Exception as pred_error:
                import traceback
                print(f"❌ Prediction error: {pred_error}")
                print(f"❌ Traceback: {traceback.format_exc()}")
                db.rollback()
                prediction_result = {"error": "Prediction failed", "details": str(pred_error)}
        else:
            print("⚠️  ML model not loaded - skipping prediction")
        
        return {
            "report_id": db_report.id,
            "message": "Report submitted successfully",
            "prediction": prediction_result
        }
        
    except Exception as e:
        print(f"❌ Submit report error: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit report: {str(e)}"
        )

# Risk prediction endpoint
@app.post("/predict-risk", response_model=schemas.RiskPredictionResponse)
async def predict_risk(
    report: schemas.ReportSubmit,
    current_user: models.User = Depends(auth.get_current_user)
):
    """Accept input features, run model inference, return full probability distribution for all disease classes"""
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="ML model not available"
        )
    
    try:
        print(f"🔮 Making prediction for user: {current_user.email}")
        
        # Preprocess input data
        processed_data = preprocess_input_data(report)
        
        # Get full prediction with all class probabilities
        prediction_result = predict_disease_probabilities(processed_data)
        
        print(f"✅ Prediction complete: {prediction_result['predicted_disease']} "
              f"({prediction_result['confidence']:.3f} confidence)")
        print(f"📊 All probabilities: {len(prediction_result['all_class_probabilities'])} classes")
        
        return schemas.RiskPredictionResponse(
            predicted_disease=prediction_result["predicted_disease"],
            confidence=round(prediction_result["confidence"], 3),
            risk_score=round(prediction_result["risk_score"], 3),
            risk_level=prediction_result["risk_level"],
            all_class_probabilities=[
                schemas.DiseaseProbability(
                    disease=prob["disease"],
                    probability=round(prob["probability"], 4)
                )
                for prob in prediction_result["all_class_probabilities"]
            ]
        )
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Risk prediction failed: {str(e)}"
        )

# Regional risk endpoint
@app.get("/regional-risk")
async def get_regional_risk(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Calculate regional risk using 7-day rolling window with trend analysis.
    Formula: (0.4 * Base_Risk) + (0.2 * Coliform) + (0.2 * Rainfall) + (0.2 * Flooding)
    Returns risk index (0-100) per region with trend indicators"""
    
    try:
        from datetime import datetime, timedelta
        
        # Define time windows
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)
        fourteen_days_ago = now - timedelta(days=14)
        
        # Get predictions from last 7 days (current window)
        current_predictions = db.query(models.Prediction).filter(
            models.Prediction.timestamp >= seven_days_ago
        ).all()
        
        # Get predictions from days 8-14 (previous window for trend)
        previous_predictions = db.query(models.Prediction).filter(
            models.Prediction.timestamp >= fourteen_days_ago,
            models.Prediction.timestamp < seven_days_ago
        ).all()
        
        # Get reports from last 7 days for water metrics
        current_reports = db.query(models.Report).filter(
            models.Report.timestamp >= seven_days_ago
        ).all()
        
        # Group current data by region
        regional_data = {}
        for pred in current_predictions:
            if pred.region not in regional_data:
                regional_data[pred.region] = {
                    'current_predictions': [],
                    'disease_counts': {},
                    'fecal_coliform_values': [],
                    'rainfall_values': [],
                    'flooding_flags': [],
                    'lat': None,
                    'lng': None
                }
            regional_data[pred.region]['current_predictions'].append(pred.risk_score / 100)
            
            # Count diseases per region
            disease = pred.predicted_disease
            if disease not in regional_data[pred.region]['disease_counts']:
                regional_data[pred.region]['disease_counts'][disease] = 0
            regional_data[pred.region]['disease_counts'][disease] += 1
        
        # Group previous data by region for trend calculation
        previous_regional_data = {}
        for pred in previous_predictions:
            if pred.region not in previous_regional_data:
                previous_regional_data[pred.region] = []
            previous_regional_data[pred.region].append(pred.risk_score / 100)
        
        # Extract water metrics and location from reports
        # Note: lat/lng are submitted but not stored in DB, using defaults per region
        region_coords = {
            'TestRegion': (28.6139, 77.2090),
            'Chennai': (13.0827, 80.2707),
            'Mumbai': (19.0760, 72.8777),
            'Delhi': (28.7041, 77.1025),
            'Bangalore': (12.9716, 77.5946),
            'Kolkata': (22.5726, 88.3639),
            'Hyderabad': (17.3850, 78.4867),
            'Ahmedabad': (23.0225, 72.5714),
            'Pune': (18.5204, 73.8567),
            'Coimbatore North': (11.0168, 76.9558)
        }
        
        for report in current_reports:
            if report.region in regional_data:
                try:
                    water_metrics = json.loads(report.water_metrics)
                    
                    # Extract fecal coliform
                    fecal_coliform = water_metrics.get('fecal_coliform_per_100ml', 0)
                    if fecal_coliform is not None:
                        regional_data[report.region]['fecal_coliform_values'].append(fecal_coliform)
                    
                    # Set default coordinates for region
                    if regional_data[report.region]['lat'] is None and report.region in region_coords:
                        regional_data[report.region]['lat'] = region_coords[report.region][0]
                        regional_data[report.region]['lng'] = region_coords[report.region][1]
                    
                except json.JSONDecodeError:
                    continue
        
        # Calculate regional risk with trend analysis
        regional_risk_results = []
        
        for region, data in regional_data.items():
            if not data['current_predictions']:
                continue
            
            # Calculate Base_Risk (average of all risk scores in last 7 days)
            base_risk = np.mean(data['current_predictions'])
            
            # Calculate normalized fecal coliform (0.2 weight)
            fecal_values = data['fecal_coliform_values']
            if fecal_values:
                avg_fecal = np.mean(fecal_values)
                normalized_fecal = min(avg_fecal / 1000, 1.0)
            else:
                normalized_fecal = 0
            
            # Use default values for rainfall and flooding (0.2 weight each)
            # TODO: Integrate with weather API for real-time data
            normalized_rainfall = 0.5  # Default moderate
            flooding_flag = 0  # Default no flooding
            
            # Apply the regional risk formula
            regional_index = (
                0.4 * base_risk +
                0.2 * normalized_fecal +
                0.2 * normalized_rainfall +
                0.2 * flooding_flag
            )
            
            # Convert to 0-100 scale
            risk_index = round(regional_index * 100, 2)
            
            # Determine risk level
            if risk_index >= 60:
                risk_level = "High"
            elif risk_index >= 30:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            # Calculate trend
            trend = "stable"
            trend_percentage = 0.0
            trend_emoji = "➖"
            
            if region in previous_regional_data and previous_regional_data[region]:
                previous_avg = np.mean(previous_regional_data[region])
                current_avg = base_risk
                
                # Calculate percentage change
                if previous_avg > 0:
                    trend_percentage = ((current_avg - previous_avg) / previous_avg) * 100
                    
                    # Determine trend direction (10% threshold)
                    if trend_percentage > 10:
                        trend = "rising"
                        trend_emoji = "📈"
                    elif trend_percentage < -10:
                        trend = "falling"
                        trend_emoji = "📉"
                    else:
                        trend = "stable"
                        trend_emoji = "➖"
            
            # Build result object
            result = {
                "region": region,
                "risk_index": risk_index,
                "risk_level": risk_level,
                "trend": trend,
                "trend_emoji": trend_emoji,
                "trend_percentage": round(trend_percentage, 2),
                "total_predictions": len(data['current_predictions']),
                "avg_fecal_coliform": round(np.mean(fecal_values), 2) if fecal_values else 0,
                "base_risk": round(base_risk * 100, 2),
                "disease_distribution": data['disease_counts']
            }
            
            # Add lat/lng if available
            if data['lat'] is not None and data['lng'] is not None:
                result["lat"] = data['lat']
                result["lng"] = data['lng']
            
            regional_risk_results.append(result)
        
        return regional_risk_results
        
    except Exception as e:
        import traceback
        print(f"❌ Regional risk calculation error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Regional risk calculation failed: {str(e)}"
        )

# Regional risk drivers endpoint (Bayesian-enhanced analysis)
@app.get("/regional-risk/{region}/drivers")
async def get_regional_risk_drivers(
    region: str,
    days: int = 7,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get top risk drivers for a specific region using hybrid Bayesian-ML analysis
    
    This endpoint combines:
    - Bayesian conditional probabilities (from training data)
    - ML model feature importance (from XGBoost)
    - Regional environmental data (from database)
    
    Requires admin authentication.
    
    Args:
        region: Region name to analyze
        days: Number of days to look back (default: 7)
    
    Returns:
        JSON with top 3 risk drivers, recommendations, and methodology
    """
    
    # Check if user is admin
    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can access regional risk driver analysis"
        )
    
    # Get the risk analyzer
    analyzer = get_analyzer()
    
    if not analyzer:
        raise HTTPException(
            status_code=503,
            detail="Bayesian Risk Analyzer not initialized. Regional driver analysis unavailable."
        )
    
    try:
        print(f"🔬 Analyzing risk drivers for {region} (last {days} days)")
        
        # Get regional drivers using hybrid analysis
        result = analyzer.get_regional_drivers(db, region, days)
        
        # Check for errors
        if 'error' in result:
            raise HTTPException(
                status_code=500,
                detail=result['error']
            )
        
        # Add methodology explanation
        result['methodology'] = {
            'description': 'Hybrid risk analysis combining Bayesian probabilities, ML feature importance, and environmental data',
            'hybrid_score_formula': 'Hybrid Score = (0.4 × Bayesian) + (0.3 × ML Importance) + (0.3 × Deviation)',
            'components': {
                'bayesian': {
                    'weight': 0.4,
                    'description': 'Conditional probability P(High Risk | Feature Elevated) from 322K training samples',
                    'source': 'Pre-calculated Bayesian probabilities based on WHO/BIS standards'
                },
                'ml_importance': {
                    'weight': 0.3,
                    'description': 'Normalized XGBoost feature importance',
                    'source': 'Trained ML model feature importance scores'
                },
                'deviation': {
                    'weight': 0.3,
                    'description': 'Distance from safe threshold (WHO/BIS standards)',
                    'source': 'Comparison of current values vs safety thresholds'
                }
            },
            'risk_levels': {
                'high_risk': 'Exceeds high_risk threshold (🔴)',
                'elevated': 'Between safe and high_risk thresholds (🟡)',
                'safe': 'Within safe limits (🟢)'
            }
        }
        
        # Add summary
        if result.get('drivers'):
            result['summary'] = {
                'region': region,
                'analysis_period_days': days,
                'reports_analyzed': result.get('report_count', 0),
                'risk_drivers_identified': len(result['drivers']),
                'top_driver': result['drivers'][0]['feature_display'] if result['drivers'] else None,
                'top_driver_score': result['drivers'][0]['hybrid_score'] if result['drivers'] else None,
                'critical_factors': len([d for d in result['drivers'] if d['hybrid_score'] > 0.7]),
                'recommendation': 'Immediate action required' if any(d['hybrid_score'] > 0.7 for d in result['drivers']) else 'Enhanced monitoring recommended'
            }
        else:
            result['summary'] = {
                'region': region,
                'analysis_period_days': days,
                'reports_analyzed': result.get('report_count', 0),
                'risk_drivers_identified': 0,
                'message': result.get('message', 'No significant risk drivers detected')
            }
        
        print(f"✅ Risk driver analysis complete for {region}")
        print(f"   Drivers identified: {len(result.get('drivers', []))}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"❌ Error in regional risk driver analysis: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Regional risk driver analysis failed: {str(e)}"
        )

# Alerts endpoint
@app.get("/alerts", response_model=List[Dict[str, Any]])
async def get_alerts(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Return active alerts where Regional Risk > 65"""
    
    try:
        # Temporarily skip check_regional_alerts to isolate the issue
        # await check_regional_alerts(db)
        
        print("📋 Fetching alerts from database...")
        
        # Get all active alerts
        db_alerts = db.query(models.Alert).filter(
            models.Alert.is_active == True
        ).order_by(models.Alert.timestamp.desc()).all()
        
        print(f"📋 Found {len(db_alerts)} active alerts")
        
        alerts = []
        for alert in db_alerts:
            print(f"  Processing alert {alert.id}: {alert.region}")
            alerts.append({
                "id": alert.id,
                "region": alert.region,
                "alert_message": alert.alert_message,
                "alert_type": alert.alert_type,
                "risk_index": None,
                "timestamp": alert.timestamp,
                "is_read": alert.is_read,
                "is_active": alert.is_active,
                "status": getattr(alert, 'status', 'active'),
                "resolved_at": getattr(alert, 'resolved_at', None),
                "resolved_by": getattr(alert, 'resolved_by', None)
            })
        
        print(f"✅ Returning {len(alerts)} alerts")
        return alerts
        
    except Exception as e:
        import traceback
        print(f"❌ ERROR in get_alerts: {str(e)}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get alerts: {str(e)}"
        )

# Create alert endpoint (admin only)
@app.post("/alerts", response_model=Dict[str, Any])
async def create_alert(
    alert: schemas.AlertCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new alert (admin only)"""
    
    print(f"🔔 Alert creation requested by {current_user.email}")
    
    # Check if user is admin
    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can create alerts"
        )
    
    # Validate required fields
    if not alert.region or not alert.region.strip():
        raise HTTPException(
            status_code=400,
            detail="Region is required"
        )
    
    if not alert.alert_message or not alert.alert_message.strip():
        raise HTTPException(
            status_code=400,
            detail="Alert message is required"
        )
    
    try:
        # Create new alert
        db_alert = models.Alert(
            region=alert.region,
            alert_message=alert.alert_message,
            alert_type=alert.alert_type or "warning",
            is_active=True,
            is_read=False,
            status="active"
        )
        
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        
        print(f"✅ Alert created: ID={db_alert.id}, Region={alert.region}, Type={alert.alert_type}")
        
        return {
            "id": db_alert.id,
            "region": db_alert.region,
            "alert_message": db_alert.alert_message,
            "alert_type": db_alert.alert_type,
            "timestamp": db_alert.timestamp,
            "is_active": db_alert.is_active,
            "message": "Alert created successfully"
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating alert: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create alert: {str(e)}"
        )

# Dismiss/Resolve alert endpoint (admin only)
@app.patch("/alerts/{alert_id}", response_model=Dict[str, Any])
async def update_alert_status(
    alert_id: int,
    alert_update: schemas.AlertUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Dismiss or resolve an alert (admin only)"""
    
    print(f"🔔 Alert update requested by {current_user.email} for alert ID {alert_id}")
    
    # Check if user is admin
    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can update alerts"
        )
    
    # Validate status
    valid_statuses = ["active", "resolved", "dismissed"]
    if alert_update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    try:
        # Find the alert
        db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
        
        if not db_alert:
            raise HTTPException(
                status_code=404,
                detail=f"Alert with ID {alert_id} not found"
            )
        
        # Update alert status
        db_alert.status = alert_update.status
        db_alert.resolved_by = alert_update.resolved_by or current_user.id
        
        # Set resolved_at timestamp if resolving or dismissing
        if alert_update.status in ["resolved", "dismissed"]:
            from datetime import datetime
            db_alert.resolved_at = datetime.utcnow()
            db_alert.is_active = False
        else:
            db_alert.resolved_at = None
            db_alert.is_active = True
        
        db.commit()
        db.refresh(db_alert)
        
        print(f"✅ Alert {alert_id} updated to status: {alert_update.status}")
        
        return {
            "id": db_alert.id,
            "region": db_alert.region,
            "alert_message": db_alert.alert_message,
            "alert_type": db_alert.alert_type,
            "status": db_alert.status,
            "resolved_at": db_alert.resolved_at,
            "resolved_by": db_alert.resolved_by,
            "timestamp": db_alert.timestamp,
            "is_active": db_alert.is_active,
            "message": f"Alert {alert_update.status} successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating alert: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update alert: {str(e)}"
        )

# Regional alert checking logic
async def check_auto_alerts(region: str, db: Session):
    """
    Check and create alerts based on:
    1. Volume Surge: >= 9 cases in 7 days
    2. AI High Risk: Average risk score >= 65%
    
    Includes 24-hour cooldown to prevent spam.
    """
    try:
        from datetime import datetime, timedelta
        
        # Define time windows
        now = datetime.now()
        start_date = now - timedelta(days=ALERT_THRESHOLDS["VOLUME_DAYS"])
        cooldown_start = now - timedelta(hours=ALERT_THRESHOLDS["COOLDOWN_HOURS"])
        
        # 1. Check Volume Surge - Count reports in the region
        case_count = db.query(models.Report).filter(
            models.Report.region == region,
            models.Report.timestamp >= start_date
        ).count()
        
        # 2. Check AI Risk - Calculate average risk score
        avg_risk_result = db.query(func.avg(models.Prediction.risk_score)).filter(
            models.Prediction.region == region,
            models.Prediction.timestamp >= start_date
        ).scalar()
        
        avg_risk = avg_risk_result if avg_risk_result is not None else 0
        
        # 3. Determine Alert Type and Priority
        alert_type = None
        alert_message = ""
        priority = "Medium"
        
        # Volume Surge takes precedence (more critical)
        if case_count >= ALERT_THRESHOLDS["VOLUME_CASES"]:
            alert_type = "Volume Surge"
            priority = "High"
            alert_message = (
                f"🚨 OUTBREAK ALERT: {case_count} cases reported in {region} "
                f"over the last {ALERT_THRESHOLDS['VOLUME_DAYS']} days "
                f"(Threshold: {ALERT_THRESHOLDS['VOLUME_CASES']} cases). "
                f"Immediate investigation and response required."
            )
            print(f"🚨 Volume Surge Detected: {region} - {case_count} cases")
            
        elif avg_risk >= ALERT_THRESHOLDS["AI_RISK_SCORE"]:
            alert_type = "AI High Risk"
            priority = "Medium"
            alert_message = (
                f"⚠️ AI RISK ALERT: Regional risk score in {region} is {avg_risk:.1f}% "
                f"(Threshold: {ALERT_THRESHOLDS['AI_RISK_SCORE']}%). "
                f"Based on {case_count} case(s) in the last {ALERT_THRESHOLDS['VOLUME_DAYS']} days. "
                f"Enhanced monitoring recommended."
            )
            print(f"⚠️  AI High Risk Detected: {region} - {avg_risk:.1f}%")
        else:
            # No alert needed
            print(f"✅ No alert needed for {region}: {case_count} cases, {avg_risk:.1f}% risk")
            return
        
        # 4. Check Cooldown - Prevent duplicate alerts
        existing_alert = db.query(models.Alert).filter(
            models.Alert.region == region,
            models.Alert.status == "active",
            models.Alert.timestamp >= cooldown_start
        ).first()
        
        if existing_alert:
            print(f"⏳ Cooldown active for {region} - Alert already exists (ID: {existing_alert.id})")
            return
        
        # 5. Create Alert
        new_alert = models.Alert(
            region=region,
            alert_type=alert_type.lower().replace(" ", "_"),  # "volume_surge" or "ai_high_risk"
            alert_message=alert_message,
            status="active",
            is_active=True
        )
        
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        
        print(f"✅ Auto-Alert Created: ID={new_alert.id}, Region={region}, Type={alert_type}, Priority={priority}")
        
        # 6. Auto-resolve old alerts if risk has dropped
        if avg_risk < 40:
            old_alerts = db.query(models.Alert).filter(
                models.Alert.region == region,
                models.Alert.status == "active",
                models.Alert.is_active == True
            ).all()
            
            for old_alert in old_alerts:
                old_alert.is_active = False
                old_alert.status = "resolved"
                old_alert.resolved_at = datetime.utcnow()
                print(f"✅ Auto-Resolved Alert: ID={old_alert.id}, Region={region} (Risk dropped to {avg_risk:.1f}%)")
            
            if old_alerts:
                db.commit()
        
    except Exception as e:
        import traceback
        print(f"❌ Error in check_auto_alerts for {region}: {str(e)}")
        print(traceback.format_exc())
        db.rollback()
        # Don't fail the request if alert checking fails


# Legacy function for backward compatibility (now calls check_auto_alerts for all regions)
async def check_regional_alerts(db: Session):
    """
    Check regional risk and create/update alerts based on:
    - Regional risk > 65: Create alert (with 24h cooldown)
    - Regional risk < 40: Auto-resolve existing alerts
    
    DEPRECATED: Use check_auto_alerts() instead for per-region checking
    """
    try:
        from datetime import datetime, timedelta
        
        # Get all unique regions from recent reports
        seven_days_ago = datetime.now() - timedelta(days=7)
        regions = db.query(models.Report.region).filter(
            models.Report.timestamp >= seven_days_ago
        ).distinct().all()
        
        # Check alerts for each region
        for (region,) in regions:
            await check_auto_alerts(region, db)
        
    except Exception as e:
        print(f"❌ Error checking regional alerts: {str(e)}")
        # Don't fail the request if alert checking fails

# New endpoint for manual alert checking
@app.post("/check-regional-alerts")
async def trigger_regional_alert_check(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Manually trigger regional alert checking"""
    
    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Only admins can trigger alert checks"
        )
    
    try:
        await check_regional_alerts(db)
        return {
            "message": "Regional alert check completed",
            "timestamp": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check regional alerts: {str(e)}"
        )

# Feature importance endpoint
@app.get("/feature-importance")
async def get_feature_importance(
    current_user: models.User = Depends(auth.get_current_user)
):
    """Return the top 10 features from the trained model"""
    
    if feature_importance_data is None:
        raise HTTPException(
            status_code=503,
            detail="Feature importance data not available"
        )
    
    try:
        # Get top 10 features
        top_features = feature_importance_data.head(10)
        
        return {
            "top_10_features": [
                {
                    "feature": row["feature"],
                    "importance": round(row["importance"], 4),
                    "importance_percentage": round(row["importance"] * 100, 2)
                }
                for _, row in top_features.iterrows()
            ],
            "model_type": type(model).__name__ if model else "Unknown",
            "total_features": len(feature_importance_data) if feature_importance_data is not None else 0
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get feature importance: {str(e)}"
        )

# Weekly reports summary endpoint
@app.get("/reports/weekly")
async def get_weekly_reports_summary(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get weekly reports summary with region breakdown, symptoms, and trends"""
    
    try:
        from datetime import datetime, timedelta
        
        # Define time windows
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)
        fourteen_days_ago = now - timedelta(days=14)
        
        # Get reports from last 7 days (current week)
        current_week_reports = db.query(models.Report).filter(
            models.Report.timestamp >= seven_days_ago
        ).all()
        
        # Get reports from previous 7 days (previous week for trend)
        previous_week_reports = db.query(models.Report).filter(
            models.Report.timestamp >= fourteen_days_ago,
            models.Report.timestamp < seven_days_ago
        ).all()
        
        # Get predictions for high-risk count
        current_week_predictions = db.query(models.Prediction).filter(
            models.Prediction.timestamp >= seven_days_ago
        ).all()
        
        # Group by region
        region_stats = {}
        for report in current_week_reports:
            if report.region not in region_stats:
                region_stats[report.region] = {
                    'count': 0,
                    'high_risk_count': 0
                }
            region_stats[report.region]['count'] += 1
        
        # Add high-risk counts from predictions
        for pred in current_week_predictions:
            if pred.region in region_stats and pred.risk_level == 'High':
                region_stats[pred.region]['high_risk_count'] += 1
        
        # Convert to list and sort by count
        by_region = [
            {
                'region': region,
                'count': stats['count'],
                'high_risk_count': stats['high_risk_count']
            }
            for region, stats in region_stats.items()
        ]
        by_region.sort(key=lambda x: x['count'], reverse=True)
        
        # Group by symptoms
        symptom_counts = {
            'diarrhea': 0,
            'vomiting': 0,
            'fever': 0,
            'abdominal_pain': 0,
            'dehydration': 0,
            'jaundice': 0,
            'bloody_stool': 0,
            'skin_rash': 0
        }
        
        for report in current_week_reports:
            try:
                symptoms = json.loads(report.symptoms)
                for symptom, value in symptoms.items():
                    if symptom in symptom_counts and value:
                        symptom_counts[symptom] += 1
            except json.JSONDecodeError:
                continue
        
        # Convert to list and sort by count
        by_symptom = [
            {'symptom': symptom, 'count': count}
            for symptom, count in symptom_counts.items()
            if count > 0
        ]
        by_symptom.sort(key=lambda x: x['count'], reverse=True)
        
        # Group by disease (from predictions)
        disease_counts = {}
        for pred in current_week_predictions:
            disease = pred.predicted_disease
            if disease not in disease_counts:
                disease_counts[disease] = 0
            disease_counts[disease] += 1
        
        # Convert to list and sort by count
        by_disease = [
            {'disease': disease, 'count': count}
            for disease, count in disease_counts.items()
        ]
        by_disease.sort(key=lambda x: x['count'], reverse=True)
        
        # Calculate trend
        current_total = len(current_week_reports)
        previous_total = len(previous_week_reports)
        
        if previous_total > 0:
            trend_percentage = ((current_total - previous_total) / previous_total) * 100
            if trend_percentage > 0:
                trend = f"+{trend_percentage:.1f}% vs previous week"
            else:
                trend = f"{trend_percentage:.1f}% vs previous week"
        else:
            trend = "No previous data"
        
        return {
            "total_reports": current_total,
            "by_region": by_region,
            "by_symptom": by_symptom,
            "by_disease": by_disease,
            "disease_distribution": disease_counts,
            "trend": trend,
            "trend_percentage": trend_percentage if previous_total > 0 else 0,
            "period": {
                "start": seven_days_ago.isoformat(),
                "end": now.isoformat()
            }
        }
        
    except Exception as e:
        import traceback
        print(f"❌ Weekly reports error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get weekly reports: {str(e)}"
        )

# Export reports endpoint
@app.get("/reports/export")
async def export_reports(
    days: int = 7,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Export reports as CSV for the specified number of days"""
    
    from fastapi.responses import StreamingResponse
    import io
    import csv
    from datetime import datetime, timedelta
    
    try:
        # Get reports from specified days
        cutoff_date = datetime.now() - timedelta(days=days)
        reports = db.query(models.Report).filter(
            models.Report.timestamp >= cutoff_date
        ).all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Region', 'District', 'Timestamp', 'User ID',
            'Diarrhea', 'Vomiting', 'Fever', 'Abdominal Pain',
            'Dehydration', 'Jaundice', 'Bloody Stool', 'Skin Rash',
            'Water Quality Index', 'pH', 'Turbidity', 'Fecal Coliform'
        ])
        
        # Write data
        for report in reports:
            try:
                symptoms = json.loads(report.symptoms)
                water_metrics = json.loads(report.water_metrics)
                
                writer.writerow([
                    report.id,
                    report.region,
                    '',  # district not stored in DB
                    report.timestamp.isoformat(),
                    report.user_id,
                    symptoms.get('diarrhea', False),
                    symptoms.get('vomiting', False),
                    symptoms.get('fever', False),
                    symptoms.get('abdominal_pain', False),
                    symptoms.get('dehydration', False),
                    symptoms.get('jaundice', False),
                    symptoms.get('bloody_stool', False),
                    symptoms.get('skin_rash', False),
                    water_metrics.get('water_quality_index', ''),
                    water_metrics.get('ph', ''),
                    water_metrics.get('turbidity_ntu', ''),
                    water_metrics.get('fecal_coliform_per_100ml', '')
                ])
            except json.JSONDecodeError:
                continue
        
        # Prepare response
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=reports_last_{days}_days.csv"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export reports: {str(e)}"
        )

# Get individual reports with predictions
@app.get("/reports/list")
async def get_reports_list(
    days: int = 7,
    region: str = None,
    risk_level: str = None,
    limit: int = 100,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of individual reports with their predictions"""
    
    try:
        from datetime import datetime, timedelta
        
        # Get reports from specified days
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Build query
        query = db.query(models.Report).filter(
            models.Report.timestamp >= cutoff_date
        )
        
        # Apply filters
        if region:
            query = query.filter(models.Report.region == region)
        
        # Order by timestamp descending (newest first)
        query = query.order_by(models.Report.timestamp.desc())
        
        # Limit results
        reports = query.limit(limit).all()
        
        # Get predictions for these reports (match by region and timestamp proximity)
        result = []
        for report in reports:
            # Find prediction for this report (within 1 minute of report timestamp)
            prediction = db.query(models.Prediction).filter(
                models.Prediction.region == report.region,
                models.Prediction.timestamp >= report.timestamp - timedelta(minutes=1),
                models.Prediction.timestamp <= report.timestamp + timedelta(minutes=1)
            ).first()
            
            # Parse symptoms
            try:
                symptoms = json.loads(report.symptoms)
            except:
                symptoms = {}
            
            # Build response object
            report_data = {
                "id": report.id,
                "region": report.region,
                "timestamp": report.timestamp.isoformat(),
                "user_id": report.user_id,
                "symptoms": symptoms,
                "predicted_disease": prediction.predicted_disease if prediction else "Unknown",
                "risk_level": prediction.risk_level if prediction else "Unknown",
                "risk_score": prediction.risk_score if prediction else 0,
                "confidence": prediction.confidence if prediction else 0
            }
            
            # Apply risk level filter if specified
            if risk_level and report_data["risk_level"] != risk_level:
                continue
            
            result.append(report_data)
        
        return {
            "reports": result,
            "total": len(result),
            "days": days,
            "filters": {
                "region": region,
                "risk_level": risk_level
            }
        }
        
    except Exception as e:
        import traceback
        print(f"❌ Get reports list error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get reports: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)