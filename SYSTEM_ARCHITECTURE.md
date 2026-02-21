# Water-Borne Disease Prediction System - System Architecture

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Web Browser                                │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │  │
│  │  │  Login Page    │  │   Community    │  │     Admin      │ │  │
│  │  │                │  │   Dashboard    │  │   Dashboard    │ │  │
│  │  │  - Auth Form   │  │  - Risk Card   │  │  - Heatmap     │ │  │
│  │  │  - Validation  │  │  - Report Form │  │  - Charts      │ │  │
│  │  │                │  │  - Alerts      │  │  - Simulation  │ │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ HTTP/HTTPS
                                  │ REST API
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              React Frontend (Port 5173)                       │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │   React    │  │   React    │  │  Tailwind  │            │  │
│  │  │  Router    │  │  Context   │  │    CSS     │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │  Recharts  │  │  Leaflet   │  │   Axios    │            │  │
│  │  │  (Charts)  │  │   (Maps)   │  │ (HTTP)     │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ JWT Token
                                  │ JSON Data
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │            FastAPI Backend (Port 8000)                        │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │    Auth    │  │   Routes   │  │  Schemas   │            │  │
│  │  │  (JWT)     │  │ (15+ APIs) │  │ (Pydantic) │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │   CORS     │  │   Error    │  │   Role     │            │  │
│  │  │ Middleware │  │  Handling  │  │   Control  │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ ORM Queries
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              SQLAlchemy ORM                                   │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │   Users    │  │  Reports   │  │Predictions │            │  │
│  │  │   Model    │  │   Model    │  │   Model    │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  │  ┌────────────┐                                             │  │
│  │  │   Alerts   │                                             │  │
│  │  │   Model    │                                             │  │
│  │  └────────────┘                                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │           SQLite Database (health_db.db)                     │  │
│  │  ┌────────────────────────────────────────────────────────┐ │  │
│  │  │  users | reports | predictions | alerts                │ │  │
│  │  └────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Model Loading
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      MACHINE LEARNING LAYER                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              ML Model Pipeline                                │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │  XGBoost   │  │  Scaler    │  │   Label    │            │  │
│  │  │   Model    │  │ (Standard) │  │  Encoder   │            │  │
│  │  │ (94.58%)   │  │            │  │            │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  │  ┌────────────┐  ┌────────────┐                            │  │
│  │  │  Feature   │  │Preprocessing│                            │  │
│  │  │   Names    │  │    Info     │                            │  │
│  │  └────────────┘  └────────────┘                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │           Model Artifacts (models/ folder)                   │  │
│  │  best_model.pkl | scaler.pkl | label_encoder.pkl            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Architecture

### **1. User Authentication Flow**

```
┌──────────┐
│  User    │
│ Browser  │
└────┬─────┘
     │ 1. Enter credentials
     ▼
┌──────────────────┐
│   Login Page     │
│  (React)         │
└────┬─────────────┘
     │ 2. POST /login
     │    {email, password}
     ▼
┌──────────────────┐
│  FastAPI         │
│  Auth Endpoint   │
└────┬─────────────┘
     │ 3. Verify credentials
     ▼
┌──────────────────┐
│  Database        │
│  (Users table)   │
└────┬─────────────┘
     │ 4. User found
     ▼
┌──────────────────┐
│  JWT Token       │
│  Generation      │
└────┬─────────────┘
     │ 5. Return token
     ▼
┌──────────────────┐
│  AuthContext     │
│  (Store token)   │
└────┬─────────────┘
     │ 6. Redirect based on role
     ▼
┌──────────────────┐     ┌──────────────────┐
│   Community      │ OR  │     Admin        │
│   Dashboard      │     │   Dashboard      │
└──────────────────┘     └──────────────────┘
```

---

### **2. Health Report Submission Flow**

```
┌──────────────────┐
│  Community User  │
│  Fills Form      │
└────┬─────────────┘
     │ 1. Submit symptoms + water data
     ▼
┌──────────────────┐
│  React Form      │
│  Validation      │
└────┬─────────────┘
     │ 2. POST /submit-report
     │    + JWT Token
     ▼
┌──────────────────┐
│  FastAPI         │
│  Verify Token    │
└────┬─────────────┘
     │ 3. Token valid
     ▼
┌──────────────────┐
│  Save Report     │
│  to Database     │
└────┬─────────────┘
     │ 4. Trigger prediction
     ▼
┌──────────────────┐
│  Preprocess      │
│  Input Data      │
└────┬─────────────┘
     │ 5. Transform features
     ▼
┌──────────────────┐
│  XGBoost Model   │
│  Prediction      │
└────┬─────────────┘
     │ 6. Disease prediction
     ▼
┌──────────────────┐
│  Calculate       │
│  Risk Score      │
└────┬─────────────┘
     │ 7. Save prediction
     ▼
┌──────────────────┐
│  Database        │
│  (Predictions)   │
└────┬─────────────┘
     │ 8. Return result
     ▼
┌──────────────────┐
│  Success         │
│  Message         │
└──────────────────┘
```

---

### **3. Regional Risk Calculation Flow**

```
┌──────────────────┐
│  Admin Dashboard │
│  Loads           │
└────┬─────────────┘
     │ 1. GET /regional-risk
     ▼
┌──────────────────┐
│  FastAPI         │
│  Endpoint        │
└────┬─────────────┘
     │ 2. Query predictions by region
     ▼
┌──────────────────┐
│  Database        │
│  Aggregate data  │
└────┬─────────────┘
     │ 3. Calculate components
     ▼
┌──────────────────────────────────────┐
│  Regional Risk Formula               │
│                                      │
│  Risk = 0.4 × mean_predicted_risk    │
│       + 0.2 × normalized_fecal       │
│       + 0.2 × normalized_rainfall    │
│       + 0.2 × flooding_flag          │
└────┬─────────────────────────────────┘
     │ 4. Risk index (0-100)
     ▼
┌──────────────────┐
│  Determine       │
│  Risk Level      │
│  (Low/Med/High)  │
└────┬─────────────┘
     │ 5. Return JSON
     ▼
┌──────────────────┐
│  React Map       │
│  Render Markers  │
└──────────────────┘
```

---

## 🏛️ Component Architecture

### **Frontend Components**

```
App.tsx (Root)
│
├── AuthProvider (Context)
│   └── AuthContext
│       ├── user state
│       ├── token state
│       ├── login()
│       └── logout()
│
├── Router
│   ├── /login
│   │   └── Login.tsx
│   │       ├── Form validation
│   │       ├── API call
│   │       └── Role-based redirect
│   │
│   ├── /community-dashboard (Protected)
│   │   └── CommunityDashboard.tsx
│   │       ├── Risk Indicator
│   │       ├── Symptom Form
│   │       ├── Education Module
│   │       └── Alerts Panel
│   │
│   └── /admin-dashboard (Protected + Admin Only)
│       └── AdminDashboard.tsx
│           ├── Statistics Cards
│           ├── Interactive Map (Leaflet)
│           ├── Rainfall Simulation
│           ├── Disease Pie Chart
│           ├── Feature Bar Chart
│           ├── Rainfall Line Chart
│           └── Alert Table
│
└── Services
    └── api.ts
        ├── authAPI
        ├── reportsAPI
        ├── predictionsAPI
        ├── alertsAPI
        └── dashboardAPI
```

---

### **Backend Components**

```
main.py (FastAPI App)
│
├── Middleware
│   ├── CORS
│   └── Error Handling
│
├── Authentication
│   ├── auth.py
│   │   ├── JWT token generation
│   │   ├── Password hashing
│   │   ├── Token verification
│   │   └── User authentication
│   │
│   └── Dependencies
│       ├── get_current_user()
│       └── verify_token()
│
├── Routes (15+ endpoints)
│   ├── /register
│   ├── /login
│   ├── /auth/me
│   ├── /submit-report
│   ├── /reports
│   ├── /predict-risk
│   ├── /predictions
│   ├── /regional-risk
│   ├── /feature-importance
│   ├── /alerts
│   └── /dashboard
│
├── Models (SQLAlchemy)
│   ├── models.py
│   │   ├── User
│   │   ├── Report
│   │   ├── Prediction
│   │   └── Alert
│   │
│   └── database.py
│       ├── Engine
│       ├── SessionLocal
│       └── get_db()
│
├── Schemas (Pydantic)
│   └── schemas.py
│       ├── UserCreate
│       ├── Login
│       ├── ReportSubmit
│       ├── PredictionResponse
│       └── AlertResponse
│
└── ML Integration
    ├── Load models at startup
    ├── Preprocess input
    ├── Make predictions
    └── Calculate risk scores
```

---

## 🗄️ Database Schema

```sql
┌─────────────────────────────────────────┐
│              users                      │
├─────────────────────────────────────────┤
│ id              INTEGER PRIMARY KEY     │
│ email           VARCHAR UNIQUE NOT NULL │
│ password_hash   VARCHAR NOT NULL        │
│ role            ENUM (community/admin)  │
│ created_at      TIMESTAMP               │
└─────────────────────────────────────────┘
                    │
                    │ 1:N
                    ▼
┌─────────────────────────────────────────┐
│             reports                     │
├─────────────────────────────────────────┤
│ id              INTEGER PRIMARY KEY     │
│ user_id         INTEGER FOREIGN KEY     │
│ region          VARCHAR NOT NULL        │
│ symptoms        TEXT (JSON)             │
│ water_metrics   TEXT (JSON)             │
│ timestamp       TIMESTAMP               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│           predictions                   │
├─────────────────────────────────────────┤
│ id                  INTEGER PRIMARY KEY │
│ region              VARCHAR NOT NULL    │
│ risk_score          FLOAT               │
│ risk_level          VARCHAR             │
│ predicted_disease   VARCHAR             │
│ confidence          FLOAT               │
│ timestamp           TIMESTAMP           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│              alerts                     │
├─────────────────────────────────────────┤
│ id              INTEGER PRIMARY KEY     │
│ region          VARCHAR NOT NULL        │
│ alert_message   TEXT NOT NULL           │
│ alert_type      VARCHAR                 │
│ timestamp       TIMESTAMP               │
│ is_read         BOOLEAN                 │
└─────────────────────────────────────────┘
```

---

## 🤖 Machine Learning Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    TRAINING PHASE                           │
└─────────────────────────────────────────────────────────────┘

Raw Data (CSV)
    │
    ▼
┌──────────────┐
│ Data Loading │
│ 322,463 rows │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Data Exploration │
│ - Check nulls    │
│ - Analyze types  │
│ - Statistics     │
└──────┬───────────┘
       │
       ▼
┌──────────────────────┐
│ Preprocessing        │
│ - Imputation         │
│ - One-hot encoding   │
│ - Label encoding     │
│ - Feature scaling    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────┐
│ Train/Test Split │
│ 80% / 20%        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Model Training   │
│ - XGBoost        │
│ - Random Forest  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Model Evaluation │
│ - Accuracy       │
│ - F1-Score       │
│ - ROC-AUC        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Select Best      │
│ XGBoost (94.58%) │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Save Artifacts   │
│ - Model          │
│ - Scaler         │
│ - Encoders       │
└──────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   PREDICTION PHASE                          │
└─────────────────────────────────────────────────────────────┘

User Input
    │
    ▼
┌──────────────────┐
│ Load Artifacts   │
│ - Model          │
│ - Scaler         │
│ - Encoders       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Preprocess Input │
│ - Same pipeline  │
│ - Feature align  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Scale Features   │
│ StandardScaler   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Model Prediction │
│ XGBoost.predict()│
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Decode Output    │
│ Label Encoder    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Calculate Risk   │
│ - Risk score     │
│ - Risk level     │
│ - Confidence     │
└──────┬───────────┘
       │
       ▼
Return Prediction
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                          │
└─────────────────────────────────────────────────────────────┘

Layer 1: Frontend Security
├── Input Validation (Pydantic schemas)
├── XSS Prevention (React escaping)
├── CSRF Protection (Token-based)
└── Secure Storage (localStorage with encryption)

Layer 2: Network Security
├── HTTPS (Production)
├── CORS Configuration
├── Rate Limiting (Future)
└── Request Validation

Layer 3: Authentication
├── JWT Tokens (HS256)
├── Token Expiration (30 min)
├── Password Hashing (PBKDF2-SHA256)
└── Secure Token Storage

Layer 4: Authorization
├── Role-Based Access Control
├── Protected Routes
├── Admin-Only Endpoints
└── User Context Verification

Layer 5: Database Security
├── SQL Injection Prevention (ORM)
├── Parameterized Queries
├── Input Sanitization
└── Data Encryption (Future)

Layer 6: API Security
├── Token Verification
├── Request Validation
├── Error Handling (No info leak)
└── Logging & Monitoring
```

---

## 📊 Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                         │
└─────────────────────────────────────────────────────────────┘

Frontend Stack
├── React 18 (UI Framework)
├── TypeScript (Type Safety)
├── Vite (Build Tool)
├── Tailwind CSS (Styling)
├── React Router (Navigation)
├── Axios (HTTP Client)
├── Recharts (Charts)
├── Leaflet (Maps)
└── Lucide React (Icons)

Backend Stack
├── Python 3.x
├── FastAPI (Web Framework)
├── SQLAlchemy (ORM)
├── SQLite (Database)
├── Pydantic (Validation)
├── Passlib (Password Hashing)
├── Python-JOSE (JWT)
└── Uvicorn (ASGI Server)

ML Stack
├── XGBoost (Model)
├── Scikit-learn (Preprocessing)
├── Pandas (Data Manipulation)
├── NumPy (Numerical Computing)
└── Joblib (Model Persistence)

Development Tools
├── Git (Version Control)
├── VS Code (IDE)
├── Postman (API Testing)
└── Chrome DevTools (Debugging)
```

---

## 🚀 Deployment Architecture (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                  PRODUCTION DEPLOYMENT                      │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │   Users      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  CDN/Nginx   │
                    │  (Static)    │
                    └──────┬───────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
        ┌──────────────┐      ┌──────────────┐
        │   Frontend   │      │   Backend    │
        │   (Vercel)   │      │  (Railway)   │
        └──────────────┘      └──────┬───────┘
                                     │
                              ┌──────┴──────┐
                              │             │
                              ▼             ▼
                      ┌──────────────┐ ┌──────────────┐
                      │  PostgreSQL  │ │    Redis     │
                      │  (Database)  │ │   (Cache)    │
                      └──────────────┘ └──────────────┘
```

---

## 📈 Performance Optimization

```
Frontend Optimizations
├── Code Splitting (React.lazy)
├── Lazy Loading (Images, Components)
├── Memoization (useMemo, useCallback)
├── Virtual Scrolling (Large lists)
└── Bundle Optimization (Vite)

Backend Optimizations
├── Database Indexing
├── Query Optimization
├── Connection Pooling
├── Caching (Future: Redis)
└── Async Operations

ML Optimizations
├── Model Compression
├── Batch Predictions
├── Feature Caching
└── Parallel Processing
```

---

## 🔄 API Request/Response Flow

```
Example: Submit Health Report

Request:
POST /submit-report
Headers:
  Authorization: Bearer eyJhbGc...
  Content-Type: application/json
Body:
{
  "region": "Chennai",
  "symptoms": {
    "diarrhea": true,
    "fever": true,
    ...
  },
  "water_metrics": {
    "water_source": "Tap",
    "ph": 7.0,
    ...
  }
}

Processing:
1. Verify JWT token
2. Extract user from token
3. Validate input (Pydantic)
4. Save to reports table
5. Preprocess for ML
6. Run prediction
7. Calculate risk
8. Save prediction
9. Check if alert needed

Response:
{
  "report_id": 123,
  "message": "Report submitted successfully",
  "prediction": {
    "prediction_id": 456,
    "predicted_disease": "Cholera",
    "risk_score": 0.85,
    "risk_level": "High",
    "confidence": 0.92
  }
}
```

---

## 📝 Summary

This system architecture demonstrates:

✅ **Separation of Concerns**: Clear layers (Client, Presentation, Application, Data, ML)

✅ **Scalability**: Modular design allows easy scaling

✅ **Security**: Multiple security layers

✅ **Maintainability**: Well-organized codebase

✅ **Performance**: Optimized at every layer

✅ **Extensibility**: Easy to add new features

---

**Last Updated**: February 20, 2026

**Version**: 1.0.0

**Status**: Production Ready ✅
