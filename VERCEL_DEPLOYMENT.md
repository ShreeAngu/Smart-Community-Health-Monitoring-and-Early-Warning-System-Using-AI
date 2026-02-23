# Vercel Deployment Guide

## Deploy to Vercel

### Prerequisites
. Vercel account: https://vercel.com/signup
. GitHub repository (already done )

---

## Step : Prepare for Deployment

### Files Created for Vercel:
- `api/main.py` - FastAPI entry point (updated)
- `vercel.json` - Vercel configuration (updated)
- `package.json` - Root package.json for workspace management (new)
- `frontend/.vercelignore` - Frontend ignore file (new)
- `requirements.txt` - Python dependencies (already existed)

---

## Step : Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

. **Go to Vercel Dashboard**
 - Visit: https://vercel.com/dashboard
 - Click "New Project"

. **Import GitHub Repository**
 - Select "Import Git Repository"
 - Choose: `Smart-Community-Health-Monitoring-and-Early-Warning-System-Using-AI`
 - Click "Import"

. **Configure Project**
 - **Framework Preset:** Other
 - **Root Directory:** Leave empty (use root)
 - **Build Command:** Leave empty (uses package.json scripts)
 - **Output Directory:** Leave empty (auto-detected)
 - **Install Command:** Leave empty (auto-detected)

. **Environment Variables** (Add these in Vercel dashboard)
 ```
 PYTHONPATH=/var/task/backend
 ```

. **Deploy**
 - Click "Deploy"
 - Wait for deployment to complete

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name: water-disease-prediction
# - Directory: ./
# - Override settings? N
```

---

## Step : Configure Domain & Settings

After deployment:

. **Custom Domain** (Optional)
 - Go to Project Settings → Domains
 - Add your custom domain

. **Environment Variables**
 - Go to Project Settings → Environment Variables
 - Add production environment variables

---

## Expected URLs

After deployment, you'll get:
- **Frontend:** `https://your-project-name.vercel.app`
- **API:** `https://your-project-name.vercel.app/api/`
- **API Docs:** `https://your-project-name.vercel.app/api/docs`

---

## Important Notes

### Limitations on Vercel

. **Database:** SQLite won't persist on Vercel (serverless)
 - **Solution:** Use PostgreSQL (Supabase, PlanetScale, or Vercel Postgres)

. **File Storage:** ML models might be too large
 - **Solution:** Store models in cloud storage (AWS S, Vercel Blob)

. **Cold Starts:** First request might be slow
 - **Solution:** Use Vercel Pro for faster cold starts

### Production Fixes Needed

#### . Database Migration (Required)

Replace SQLite with PostgreSQL:

```python
# In backend/database.py
import os

DATABASE_URL = os.getenv(
 "DATABASE_URL",
 "postgresql://user:password@host:port/dbname"
)
```

#### . Model Storage (If models are large)

Store models in Vercel Blob or AWS S:

```python
# In backend/ml_engine.py
import requests
import os

def load_model_from_url():
 model_url = os.getenv("MODEL_URL")
 response = requests.get(model_url)
 # Load model from response.content
```

#### . Environment Variables

Add to Vercel dashboard:
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
MODEL_URL=https://...
```

---

## Testing Deployment

After deployment, test these endpoints:

```bash
# Health check
curl https://your-app.vercel.app/api/

# API docs
curl https://your-app.vercel.app/api/docs

# Login endpoint
curl -X POST https://your-app.vercel.app/api/login \
 -H "Content-Type: application/json" \
 -d '{"email":"admin@example.com","password":"admin"}'
```

---

## Troubleshooting

### Common Issues:

. **"No FastAPI entrypoint found"**
 - Fixed with `api/main.py`
 - Updated `vercel.json` configuration
 - Added proper Python path handling

. **"Module not found"**
 - Check `PYTHONPATH` environment variable
 - Ensure all imports use relative paths
 - Fixed with updated `api/main.py`

. **"Build failed - npm install"**
 - Fixed with proper build configuration
 - Added root `package.json` for workspace management
 - Updated `vercel.json` to handle both Python and Node.js builds

. **"Database locked"**
 - SQLite doesn't work on serverless
 - Migrate to PostgreSQL for production

. **"Function timeout"**
 - Increase timeout in `vercel.json`
 - Optimize ML model loading

. **Python Dependencies Installation**
 - Vercel automatically installs from `requirements.txt`
 - No manual pip install needed in `vercel.json`

. **Node.js Dependencies Installation**
 - Vercel automatically detects `frontend/package.json`
 - Runs `npm install` and `npm run build` automatically

---

## Alternative: Separate Deployments

If full-stack deployment is complex, deploy separately:

### Frontend Only on Vercel:
```bash
cd frontend
vercel
```

### Backend on Railway/Render:
- Railway: https://railway.app
- Render: https://render.com
- Both support FastAPI with persistent databases

---

## Production Checklist

Before going live:

- [ ] Migrate to PostgreSQL database
- [ ] Set up proper environment variables
- [ ] Configure CORS for production domain
- [ ] Set up monitoring (Sentry)
- [ ] Add rate limiting
- [ ] Set up SSL certificates
- [ ] Configure custom domain
- [ ] Test all API endpoints
- [ ] Test frontend functionality
- [ ] Set up backup strategy

---

## Cost Estimation

**Vercel Free Tier:**
- 00GB bandwidth/month
- 00 deployments/day
- Serverless functions
- Limited to 0s function execution

**Vercel Pro ($0/month):**
- TB bandwidth
- Faster builds
- 0s function execution
- Analytics

---

**Ready to deploy? Follow the steps above! **