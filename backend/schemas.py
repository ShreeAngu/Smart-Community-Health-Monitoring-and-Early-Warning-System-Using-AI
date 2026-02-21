from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    community = "community"
    admin = "admin"

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.community

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth schemas
class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Report schemas
class WaterMetrics(BaseModel):
    ph: Optional[float] = None
    turbidity_ntu: Optional[float] = None
    dissolved_oxygen_mg_l: Optional[float] = None
    bod_mg_l: Optional[float] = None
    fecal_coliform_per_100ml: Optional[int] = None
    total_coliform_per_100ml: Optional[int] = None
    tds_mg_l: Optional[float] = None
    nitrate_mg_l: Optional[float] = None
    fluoride_mg_l: Optional[float] = None
    arsenic_ug_l: Optional[float] = None
    water_quality_index: Optional[float] = None

class Symptoms(BaseModel):
    diarrhea: bool = False
    vomiting: bool = False
    fever: bool = False
    abdominal_pain: bool = False
    dehydration: bool = False
    jaundice: bool = False
    bloody_stool: bool = False
    skin_rash: bool = False

class ReportSubmit(BaseModel):
    region: str
    district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_urban: Optional[bool] = None
    population_density: Optional[int] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    water_source: Optional[str] = None
    water_treatment: Optional[str] = None
    water_metrics: WaterMetrics
    symptoms: Symptoms
    # Environmental factors
    open_defecation_rate: Optional[float] = None
    toilet_access: Optional[int] = None
    sewage_treatment_pct: Optional[float] = None
    handwashing_practice: Optional[str] = None
    month: Optional[int] = None
    season: Optional[str] = None
    avg_temperature_c: Optional[float] = None
    avg_rainfall_mm: Optional[float] = None
    avg_humidity_pct: Optional[float] = None
    flooding: Optional[bool] = None

class ReportResponse(BaseModel):
    id: int
    region: str
    symptoms: Dict[str, Any]
    water_metrics: Dict[str, Any]
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Prediction schemas
class DiseaseProbability(BaseModel):
    disease: str
    probability: float

class PredictionResponse(BaseModel):
    id: int
    region: str
    risk_score: float
    risk_level: str
    predicted_disease: Optional[str] = None
    confidence: Optional[float] = None
    all_class_probabilities: Optional[List[DiseaseProbability]] = None
    timestamp: datetime
    recommendations: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

class RiskPredictionResponse(BaseModel):
    """Response for /predict-risk endpoint with full probability distribution"""
    predicted_disease: str
    confidence: float
    risk_score: float
    risk_level: str
    all_class_probabilities: List[DiseaseProbability]

class PredictionRequest(BaseModel):
    report_data: ReportSubmit

# Alert schemas
class AlertResponse(BaseModel):
    id: int
    region: str
    alert_message: str
    alert_type: str
    timestamp: datetime
    is_read: bool
    status: Optional[str] = "active"
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    
    class Config:
        from_attributes = True

class AlertCreate(BaseModel):
    region: str
    alert_message: str
    alert_type: str = "warning"

class AlertUpdate(BaseModel):
    status: str  # active, resolved, dismissed
    resolved_by: Optional[int] = None

# Dashboard schemas
class DashboardStats(BaseModel):
    total_reports: int
    total_predictions: int
    high_risk_regions: int
    recent_alerts: int
    disease_distribution: Dict[str, int]
    risk_by_region: Dict[str, str]