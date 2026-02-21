# Water-Borne Disease Prediction Backend

FastAPI backend for the Water-Borne Disease Prediction system.

## Features

- **Authentication**: JWT-based authentication with user roles (community/admin)
- **Disease Prediction**: ML-powered disease prediction using XGBoost
- **Data Management**: SQLite database for reports, predictions, and alerts
- **RESTful API**: Complete CRUD operations for all entities
- **Real-time Alerts**: Alert system for high-risk predictions

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Start the Server**:
   ```bash
   python start_server.py
   ```

3. **Access API Documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info

### Reports
- `POST /reports` - Submit health report
- `GET /reports` - Get user reports

### Predictions
- `POST /predict` - Make disease prediction
- `GET /predictions` - Get prediction history

### Alerts
- `GET /alerts` - Get alerts
- `POST /alerts` - Create alert (admin only)

### Dashboard
- `GET /dashboard` - Get dashboard statistics

## Database Schema

### Users
- id, email, password_hash, role, created_at

### Reports
- id, user_id, region, symptoms (JSON), water_metrics (JSON), timestamp

### Predictions
- id, region, risk_score, risk_level, predicted_disease, confidence, timestamp

### Alerts
- id, region, alert_message, alert_type, timestamp, is_read

## ML Model

The system uses an XGBoost classifier trained on water quality and health data:
- **Accuracy**: 94.58%
- **ROC-AUC**: 99.76%
- **Classes**: 8 disease types + No_Disease

## Security

- Password hashing with bcrypt
- JWT tokens for authentication
- Role-based access control
- Input validation with Pydantic

## Testing

The backend includes comprehensive testing scripts to verify all functionality.

### Setup Demo Users

Before running tests, create demo users:

```bash
python create_demo_users.py
```

This creates three test accounts:
- **Admin**: admin@example.com / admin123
- **Community**: community@example.com / community123  
- **Test**: test@example.com / testpassword123

Expected output:
```
✓ DEMO USERS CREATED SUCCESSFULLY!
✓ All users verified successfully!
✅ SETUP COMPLETE - READY TO USE!
```

### Test Scripts

#### 1. Endpoint Testing (`test_endpoints.py`)

Tests all API endpoints with valid and invalid inputs:

```bash
python test_endpoints.py
```

Tests include:
- Health check endpoint
- Login with valid/invalid credentials
- Submit health report
- Predict disease risk
- Regional risk calculation (verifies formula)
- Feature importance
- Alerts (admin and community access)
- Dashboard statistics
- Unauthorized access handling

Expected output:
```
✓ PASS - GET /health
✓ PASS - POST /login (valid)
✓ PASS - POST /login (invalid)
✓ PASS - POST /submit-report
✓ PASS - POST /predict-risk
✓ PASS - GET /regional-risk
✓ PASS - GET /feature-importance
✓ PASS - GET /alerts (admin)
✓ PASS - GET /alerts (community)
✓ PASS - GET /dashboard
✓ PASS - GET /dashboard (no token)

✅ ALL TESTS PASSED!
```

Exit codes:
- `0` - All tests passed
- `1` - Some tests failed

#### 2. Role-Based Access Testing (`test_role_based_login.py`)

Tests authentication and role-based access control:

```bash
python test_role_based_login.py
```

Tests include:
- User authentication and role verification
- Admin access to protected endpoints
- Community user restrictions
- Invalid token handling
- No token access
- Token expiration (manual test guidance)

Expected output:
```
✓ PASS User Authentication
✓ PASS Admin Endpoint Access
✓ PASS Community User Restrictions
✓ PASS Invalid Token Handling
✓ PASS No Token Access
✓ PASS Token Expiration (Manual)

✅ ALL TESTS PASSED!
```

Exit codes:
- `0` - All tests passed
- `1` - Some tests failed

#### 3. Quick Setup Test (`test_setup.py`)

Quick verification that the server is running:

```bash
python test_setup.py
```

### Running All Tests

To run all tests in sequence:

```bash
# Windows CMD
python create_demo_users.py & python test_endpoints.py & python test_role_based_login.py

# Windows PowerShell
python create_demo_users.py; python test_endpoints.py; python test_role_based_login.py
```

### Test Requirements

All test scripts require:
- Backend server running on `http://localhost:8000`
- Demo users created (run `create_demo_users.py` first)
- `requests` library installed (`pip install requests`)

### Manual Testing

For manual API testing, use the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Token Expiration Testing

To manually test token expiration:

1. Edit `auth.py` and set `ACCESS_TOKEN_EXPIRE_MINUTES = 1`
2. Restart the server
3. Login and save the token
4. Wait 2 minutes
5. Try accessing a protected endpoint
6. Should receive `401 Unauthorized`
7. Restore `ACCESS_TOKEN_EXPIRE_MINUTES` to 30

## Development

Start with auto-reload:
```bash
python start_server.py
```

The server will automatically reload when you make changes to the code.