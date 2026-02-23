# Water-Borne Disease Prediction System

An AI-powered health monitoring system for predicting and tracking water-borne diseases using machine learning, Bayesian analysis, and real-time data visualization.

![Python](https://img.shields.io/badge/python-.+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.0+-green.svg)
![React](https://img.shields.io/badge/React-.+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## Table of Contents

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

## Overview

This system provides early detection and monitoring of water-borne diseases (Cholera, Typhoid, Hepatitis A, Dysentery) by analyzing water quality parameters, environmental factors, and health symptoms. It combines machine learning predictions with Bayesian probability analysis to provide actionable insights for health authorities and communities.

### Key Capabilities

- **AI-Powered Predictions** - XGBoost model with % accuracy
- **Real-Time Monitoring** - Live regional risk assessment
- **Interactive Maps** - Geographic risk visualization
- **Trend Analysis** - -day rolling window with trend indicators
- **Smart Alerts** - Automated alerts for high-risk regions
- **Dual Dashboards** - Separate interfaces for admins and community users

---

## Features

### For Health Authorities (Admin Dashboard)

- **Regional Risk Heatmap** - Interactive map showing risk levels across regions
- **AI Risk Analysis** - Bayesian + ML hybrid analysis of risk drivers
- **Alert Management** - Create, dismiss, and resolve health alerts
- **Weekly Reports** - Comprehensive summaries with disease distribution
- **Disease Analytics** - Charts showing disease patterns and trends
- **Live Data Sync** - Real-time updates every 0 seconds

### For Community Users

- **Symptom Reporting** - Easy-to-use health report submission
- **Risk Assessment** - Instant ML-based disease prediction
- **Health Alerts** - View active alerts for your region
- **Health Education** - Tips for disease prevention
- **Privacy-First** - Anonymous reporting option

---

## Tech Stack

### Backend
- **Framework:** FastAPI (Python .+)
- **Database:** SQLite with SQLAlchemy ORM
- **ML/AI:** XGBoost, scikit-learn, NumPy, Pandas
- **Authentication:** JWT tokens with bcrypt
- **API:** RESTful with automatic OpenAPI documentation

### Frontend
- **Framework:** React . with TypeScript
- **Routing:** React Router v
- **Maps:** Leaflet with React-Leaflet
- **Charts:** Recharts
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Build:** Vite

### ML Pipeline
- **Algorithm:** XGBoost Classifier
- **Features:** + parameters (water quality, demographics, symptoms)
- **Classes:** diseases (Cholera, Typhoid, Hepatitis A, Dysentery, No Disease)
- **Accuracy:** ~%
- **Bayesian Analysis:** Conditional probability calculations

---

## System Architecture

```

 Frontend (React)

 Admin Dashboard Community Portal
 - Risk Maps - Report Form
 - Analytics - Predictions
 - Alerts - Alerts

 REST API (FastAPI)

 Backend Services

 ML Engine Bayesian Alert
 - XGBoost Analyzer System
 - Predict - Risk - Monitor
 - Preprocess - Drivers - Notify

 Database
 (SQLite)
 - Users
 - Reports
 - Predictions
 - Alerts

```

---

## Installation

### Prerequisites

- Python . or higher
- Node.js or higher
- npm or yarn
- Git

### Step : Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/water-disease-prediction.git
cd water-disease-prediction
```

### Step : Backend Setup

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

Backend will run on: `http://localhost:000`

### Step : Frontend Setup

```bash
# Navigate to frontend (in new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:`

---

## Usage

### Access the Application

. **Admin Dashboard:** `http://localhost:/admin-dashboard`
 - Email: `admin@example.com`
 - Password: `admin`

. **Community Dashboard:** `http://localhost:/community-dashboard`
 - Email: `community@example.com`
 - Password: `community`

### Submit a Health Report

. Login to Community Dashboard
. Fill in the report form:
 - Location (Region, District)
 - Personal Info (Age, Gender)
 - Water Quality (pH, Turbidity, Fecal Coliform, etc.)
 - Symptoms (Diarrhea, Vomiting, Fever, etc.)
 - Environmental Factors (Temperature, Rainfall, Flooding)
. Submit and get instant AI prediction

### View Regional Risk

. Login to Admin Dashboard
. View interactive risk heatmap
. Click on region markers for details
. Click "View AI Risk Analysis" for Bayesian analysis

### Manage Alerts

. Admin Dashboard → Alerts section
. Create new alerts for high-risk regions
. Dismiss false positives
. Resolve addressed alerts

---

## API Documentation

### Base URL
```
http://localhost:000
```

### Authentication
```bash
POST /login
Content-Type: application/json

{
 "email": "admin@example.com",
 "password": "admin"
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

Visit `http://localhost:000/docs` for Swagger UI documentation.

---

## Project Structure

```
water-disease-prediction/
 backend/
 main.py # FastAPI application
 models.py # Database models
 schemas.py # Pydantic schemas
 auth.py # Authentication
 database.py # Database connection
 ml_engine.py # ML prediction engine
 calculate_bayesian_probs.py # Bayesian analysis
 models/ # Trained ML models
 best_model.pkl
 scaler.pkl
 label_encoder.pkl
 bayesian_probs.json
 utils/
 csv_sync.py # CSV synchronization
 column_mapping.py # Column name mapping
 tests/ # Test files

 frontend/
 src/
 components/ # React components
 BayesianDriversModal.tsx
 WeeklyReports.tsx
 ...
 pages/ # Page components
 AdminDashboard.tsx
 CommunityDashboard.tsx
 Login.tsx
 context/ # React context
 AuthContext.tsx
 services/ # API services
 api.ts
 App.tsx # Main app component
 public/ # Static assets
 package.json # Dependencies

 Data/
 water_disease_data.csv # Training dataset

 docs/ # Documentation
 README.md # This file
 SYSTEM_ARCHITECTURE.md # Architecture details
 requirements.txt # Python dependencies
 .gitignore # Git ignore rules
 train_model.py # ML model training script
```

---

## ML Model

### Training Data

- **Dataset Size:** 0,000+ samples
- **Features:** parameters
 - Water Quality: pH, turbidity, fecal coliform, TDS, nitrate, arsenic, etc.
 - Demographics: Age, gender, population density
 - Sanitation: Toilet access, handwashing, sewage treatment
 - Environmental: Temperature, rainfall, humidity, flooding
 - Symptoms: Diarrhea, vomiting, fever, abdominal pain, etc.

### Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | .% |
| Precision | .% |
| Recall | .% |
| F-Score | .% |

### Risk Index Calculation

```
Risk Index = (0. × Base_Risk) + (0. × Coliform) + (0. × Rainfall) + (0. × Flooding)
```

Where:
- **Base_Risk:** Average ML predictions (last days)
- **Coliform:** Normalized fecal coliform level
- **Rainfall:** Normalized rainfall amount
- **Flooding:** Binary flooding indicator

### Risk Levels

| Risk Index | Level | Color | Action |
|------------|-------|-------|--------|
| ≥0% | High | Red | Immediate intervention |
| 0-% | Medium | Yellow | Enhanced monitoring |
| <0% | Low | Green | Routine surveillance |

---

## Testing

### Backend Tests

```bash
cd backend/tests
python test_endpoints.py
python test_ml_engine.py
```

### Seed Test Data

```bash
cd backend
python seed_high_risk_reports.py # Create high-risk test data
python seed_extreme_risk.py # Create extreme scenarios
```

### Verify Setup

```bash
python verify_users.py # Check user accounts
python verify_frontend_data.py # Verify API responses
```

---

## Security

- **Authentication:** JWT tokens with secure password hashing (bcrypt)
- **Authorization:** Role-based access control (Admin/Community)
- **Data Privacy:** Anonymous reporting option
- **Input Validation:** Pydantic schemas for all API inputs
- **SQL Injection:** Protected by SQLAlchemy ORM
- **CORS:** Configured for frontend-backend communication

---

## Deployment

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

## Contributing

Contributions are welcome! Please follow these steps:

. Fork the repository
. Create a feature branch (`git checkout -b feature/AmazingFeature`)
. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
. Push to the branch (`git push origin feature/AmazingFeature`)
. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

---

## Acknowledgments

- XGBoost team for the excellent ML library
- FastAPI for the modern Python web framework
- React team for the powerful UI library
- Leaflet for interactive maps
- All contributors and testers

---

## Support

For support, email your.email@example.com or open an issue on GitHub.

---

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Weather API integration for real-time rainfall data
- [ ] SMS alerts for critical situations
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Export reports to PDF
- [ ] Integration with government health systems
- [ ] Machine learning model retraining pipeline

---

## Statistics

- **Lines of Code:** ~,000+
- **API Endpoints:** 0+
- **React Components:** +
- **ML Features:** +
- **Supported Diseases:**
- **Regions Covered:** Tamil Nadu, India

---

**Made with care for public health**
