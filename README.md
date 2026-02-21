# 💧 Water-Borne Disease Prediction System

An AI-powered health monitoring system for predicting and tracking water-borne diseases using machine learning, Bayesian analysis, and real-time data visualization.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![React](https://img.shields.io/badge/React-18.2+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [ML Model](#ml-model)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

This system provides early detection and monitoring of water-borne diseases (Cholera, Typhoid, Hepatitis A, Dysentery) by analyzing water quality parameters, environmental factors, and health symptoms. It combines machine learning predictions with Bayesian probability analysis to provide actionable insights for health authorities and communities.

### Key Capabilities

- 🤖 **AI-Powered Predictions** - XGBoost model with 95% accuracy
- 📊 **Real-Time Monitoring** - Live regional risk assessment
- 🗺️ **Interactive Maps** - Geographic risk visualization
- 📈 **Trend Analysis** - 7-day rolling window with trend indicators
- 🚨 **Smart Alerts** - Automated alerts for high-risk regions
- 📱 **Dual Dashboards** - Separate interfaces for admins and community users

---

## ✨ Features

### For Health Authorities (Admin Dashboard)

- **Regional Risk Heatmap** - Interactive map showing risk levels across regions
- **AI Risk Analysis** - Bayesian + ML hybrid analysis of risk drivers
- **Alert Management** - Create, dismiss, and resolve health alerts
- **Weekly Reports** - Comprehensive summaries with disease distribution
- **Disease Analytics** - Charts showing disease patterns and trends
- **Live Data Sync** - Real-time updates every 10 seconds

### For Community Users

- **Symptom Reporting** - Easy-to-use health report submission
- **Risk Assessment** - Instant ML-based disease prediction
- **Health Alerts** - View active alerts for your region
- **Health Education** - Tips for disease prevention
- **Privacy-First** - Anonymous reporting option

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.8+)
- **Database:** SQLite with SQLAlchemy ORM
- **ML/AI:** XGBoost, scikit-learn, NumPy, Pandas
- **Authentication:** JWT tokens with bcrypt
- **API:** RESTful with automatic OpenAPI documentation

### Frontend
- **Framework:** React 18.2 with TypeScript
- **Routing:** React Router v6
- **Maps:** Leaflet with React-Leaflet
- **Charts:** Recharts
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Build:** Vite

### ML Pipeline
- **Algorithm:** XGBoost Classifier
- **Features:** 45+ parameters (water quality, demographics, symptoms)
- **Classes:** 5 diseases (Cholera, Typhoid, Hepatitis A, Dysentery, No Disease)
- **Accuracy:** ~95%
- **Bayesian Analysis:** Conditional probability calculations

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │ Admin Dashboard  │         │ Community Portal │         │
│  │  - Risk Maps     │         │  - Report Form   │         │
│  │  - Analytics     │         │  - Predictions   │         │
│  │  - Alerts        │         │  - Alerts        │         │
│  └──────────────────┘         └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            │
                    REST API (FastAPI)
                            │
┌─────────────────────────────────────────────────────────────┐
│                     Backend Services                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  ML Engine   │  │  Bayesian    │  │  Alert       │     │
│  │  - XGBoost   │  │  Analyzer    │  │  System      │     │
│  │  - Predict   │  │  - Risk      │  │  - Monitor   │     │
│  │  - Preprocess│  │  - Drivers   │  │  - Notify    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                    ┌───────────────┐
                    │   Database    │
                    │   (SQLite)    │
                    │  - Users      │
                    │  - Reports    │
                    │  - Predictions│
                    │  - Alerts     │
                    └───────────────┘
```

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/water-disease-prediction.git
cd water-disease-prediction
```

### Step 2: Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Navigate to backend
cd backend

# Create demo users and database
python create_demo_users.py

# Start backend server
python start_server.py
```

Backend will run on: `http://localhost:8000`

### Step 3: Frontend Setup

```bash
# Navigate to frontend (in new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:5173`

---

## 🚀 Usage

### Access the Application

1. **Admin Dashboard:** `http://localhost:5173/admin-dashboard`
   - Email: `admin@example.com`
   - Password: `admin123`

2. **Community Dashboard:** `http://localhost:5173/community-dashboard`
   - Email: `community@example.com`
   - Password: `community123`

### Submit a Health Report

1. Login to Community Dashboard
2. Fill in the report form:
   - Location (Region, District)
   - Personal Info (Age, Gender)
   - Water Quality (pH, Turbidity, Fecal Coliform, etc.)
   - Symptoms (Diarrhea, Vomiting, Fever, etc.)
   - Environmental Factors (Temperature, Rainfall, Flooding)
3. Submit and get instant AI prediction

### View Regional Risk

1. Login to Admin Dashboard
2. View interactive risk heatmap
3. Click on region markers for details
4. Click "View AI Risk Analysis" for Bayesian analysis

### Manage Alerts

1. Admin Dashboard → Alerts section
2. Create new alerts for high-risk regions
3. Dismiss false positives
4. Resolve addressed alerts

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication
```bash
POST /login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "admin123"
}
```

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | User authentication |
| POST | `/reports/submit` | Submit health report |
| GET | `/predictions/predict` | Get disease prediction |
| GET | `/regional-risk` | Get regional risk data |
| GET | `/regional-risk/{region}/drivers` | Get risk drivers |
| GET | `/alerts` | Get all alerts |
| POST | `/alerts` | Create new alert |
| GET | `/reports/weekly` | Get weekly summary |
| GET | `/reports/list` | List recent reports |

### Interactive API Docs

Visit `http://localhost:8000/docs` for Swagger UI documentation.

---

## 📁 Project Structure

```
water-disease-prediction/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   ├── auth.py                 # Authentication
│   ├── database.py             # Database connection
│   ├── ml_engine.py            # ML prediction engine
│   ├── calculate_bayesian_probs.py  # Bayesian analysis
│   ├── models/                 # Trained ML models
│   │   ├── best_model.pkl
│   │   ├── scaler.pkl
│   │   ├── label_encoder.pkl
│   │   └── bayesian_probs.json
│   ├── utils/
│   │   ├── csv_sync.py         # CSV synchronization
│   │   └── column_mapping.py   # Column name mapping
│   └── tests/                  # Test files
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── BayesianDriversModal.tsx
│   │   │   ├── WeeklyReports.tsx
│   │   │   └── ...
│   │   ├── pages/              # Page components
│   │   │   ├── AdminDashboard.tsx
│   │   │   ├── CommunityDashboard.tsx
│   │   │   └── Login.tsx
│   │   ├── context/            # React context
│   │   │   └── AuthContext.tsx
│   │   ├── services/           # API services
│   │   │   └── api.ts
│   │   └── App.tsx             # Main app component
│   ├── public/                 # Static assets
│   └── package.json            # Dependencies
│
├── Data/
│   └── water_disease_data.csv  # Training dataset
│
├── docs/                       # Documentation
├── README.md                   # This file
├── SYSTEM_ARCHITECTURE.md      # Architecture details
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── train_model.py              # ML model training script
```

---

## 🤖 ML Model

### Training Data

- **Dataset Size:** 10,000+ samples
- **Features:** 45 parameters
  - Water Quality: pH, turbidity, fecal coliform, TDS, nitrate, arsenic, etc.
  - Demographics: Age, gender, population density
  - Sanitation: Toilet access, handwashing, sewage treatment
  - Environmental: Temperature, rainfall, humidity, flooding
  - Symptoms: Diarrhea, vomiting, fever, abdominal pain, etc.

### Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 95.2% |
| Precision | 93.4% |
| Recall | 94.1% |
| F1-Score | 93.7% |

### Risk Index Calculation

```
Risk Index = (0.4 × Base_Risk) + (0.2 × Coliform) + (0.2 × Rainfall) + (0.2 × Flooding)
```

Where:
- **Base_Risk:** Average ML predictions (last 7 days)
- **Coliform:** Normalized fecal coliform level
- **Rainfall:** Normalized rainfall amount
- **Flooding:** Binary flooding indicator

### Risk Levels

| Risk Index | Level | Color | Action |
|------------|-------|-------|--------|
| ≥60% | High | 🔴 Red | Immediate intervention |
| 30-59% | Medium | 🟡 Yellow | Enhanced monitoring |
| <30% | Low | 🟢 Green | Routine surveillance |

---

## 🧪 Testing

### Backend Tests

```bash
cd backend/tests
python test_endpoints.py
python test_ml_engine.py
```

### Seed Test Data

```bash
cd backend
python seed_high_risk_reports.py  # Create high-risk test data
python seed_extreme_risk.py        # Create extreme scenarios
```

### Verify Setup

```bash
python verify_users.py             # Check user accounts
python verify_frontend_data.py     # Verify API responses
```

---

## 🔒 Security

- **Authentication:** JWT tokens with secure password hashing (bcrypt)
- **Authorization:** Role-based access control (Admin/Community)
- **Data Privacy:** Anonymous reporting option
- **Input Validation:** Pydantic schemas for all API inputs
- **SQL Injection:** Protected by SQLAlchemy ORM
- **CORS:** Configured for frontend-backend communication

---

## 🌍 Deployment

### Production Checklist

- [ ] Set environment variables (SECRET_KEY, DATABASE_URL)
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up proper CORS origins
- [ ] Configure logging
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Use production build for frontend (`npm run build`)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure firewall rules

### Docker Deployment (Optional)

```dockerfile
# Coming soon
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- XGBoost team for the excellent ML library
- FastAPI for the modern Python web framework
- React team for the powerful UI library
- Leaflet for interactive maps
- All contributors and testers

---

## 📞 Support

For support, email your.email@example.com or open an issue on GitHub.

---

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Weather API integration for real-time rainfall data
- [ ] SMS alerts for critical situations
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Export reports to PDF
- [ ] Integration with government health systems
- [ ] Machine learning model retraining pipeline

---

## 📊 Statistics

- **Lines of Code:** ~15,000+
- **API Endpoints:** 20+
- **React Components:** 15+
- **ML Features:** 45+
- **Supported Diseases:** 5
- **Regions Covered:** Tamil Nadu, India

---

**Made with ❤️ for public health**
