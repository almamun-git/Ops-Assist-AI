# Deployment Guide - Ops-Assist AI

Complete guide to deploy Ops-Assist AI to production cloud platforms.

## 🌐 Deployment Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │──────│   Backend   │──────│  Database   │
│   (Vercel)  │      │  (Railway)  │      │ (Supabase)  │
│  Next.js    │      │  FastAPI    │      │ PostgreSQL  │
└─────────────┘      └─────────────┘      └─────────────┘
```

**Why this stack?**
- ✅ All have **free tiers**
- ✅ Auto-deployment from GitHub
- ✅ Production-ready with SSL
- ✅ Easy scaling
- ✅ No server management

---

## 📦 Deployment Options

### Option A: Free Tier (Recommended for Learning)
- **Frontend**: Vercel (Free)
- **Backend**: Railway (Free $5/month credit)
- **Database**: Supabase (Free 500MB)

### Option B: Professional
- **Frontend**: Vercel Pro ($20/month)
- **Backend**: Railway ($5-20/month based on usage)
- **Database**: Supabase Pro ($25/month)

### Option C: Enterprise
- **Frontend**: AWS Amplify
- **Backend**: AWS ECS/Lambda
- **Database**: AWS RDS

---

## 🚀 Step-by-Step Deployment

## Part 1: Deploy Database (Supabase)

### 1. Create Supabase Account
1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub

### 2. Create New Project
```
Project Name: ops-assist-ai
Database Password: [choose strong password]
Region: [closest to your users]
```

### 3. Get Database URL
1. Go to Project Settings → Database
2. Copy the **Connection String** (URI format)
3. It looks like:
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### 4. Run Database Migrations
```bash
# Update DATABASE_URL in .env with Supabase URL
cd apps/backend

# Run migrations (creates tables)
venv/bin/alembic upgrade head

# Or manually create tables with Python
venv/bin/python -c "
from src.core.database import engine
from src.models import Base
Base.metadata.create_all(bind=engine)
"
```

---

## Part 2: Deploy Backend (Railway)

### 1. Prepare Backend for Deployment

Create `apps/backend/Procfile`:
```bash
web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

Create `apps/backend/railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn src.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Update requirements.txt
Make sure it includes:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
openai==1.3.0
alembic==1.12.1
```

### 3. Deploy to Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `Ops-Assist-AI` repository
5. Configure:
   - **Root Directory**: `apps/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

### 4. Add Environment Variables

In Railway dashboard, add these variables:

```bash
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
OPENAI_API_KEY=sk-your-openai-key
INCIDENT_THRESHOLD=5
INCIDENT_TIME_WINDOW=300
PYTHON_VERSION=3.11
```

### 5. Get Backend URL

Railway will provide a URL like:
```
https://ops-assist-ai-backend.up.railway.app
```

---

## Part 3: Deploy Frontend (Vercel)

### 1. Update Frontend Configuration

Update `apps/frontend/.env.production`:
```bash
NEXT_PUBLIC_API_URL=https://ops-assist-ai-backend.up.railway.app
```

### 2. Update Backend CORS

Update `apps/backend/src/main.py`:
```python
# Add your Vercel domain to CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ops-assist-ai.vercel.app",  # Add your Vercel domain
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Deploy to Vercel

#### Option 1: Using Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from frontend directory
cd apps/frontend
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: ops-assist-ai
# - Directory: ./
# - Override settings? No
```

#### Option 2: Using Vercel Dashboard
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "New Project"
4. Import `Ops-Assist-AI` repository
5. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `apps/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 4. Add Environment Variables

In Vercel dashboard, add:
```bash
NEXT_PUBLIC_API_URL=https://ops-assist-ai-backend.up.railway.app
```

### 5. Deploy!

Vercel will provide URLs:
```
Production: https://ops-assist-ai.vercel.app
Preview: https://ops-assist-ai-git-main-username.vercel.app
```

---

## 🔧 Post-Deployment Configuration

### 1. Update Backend CORS (Important!)

```bash
# Commit the CORS update
git add apps/backend/src/main.py
git commit -m "chore: add production CORS origins"
git push origin main
```

Railway will auto-deploy the update.

### 2. Test the Deployment

```bash
# Test backend health
curl https://ops-assist-ai-backend.up.railway.app/health

# Test frontend
open https://ops-assist-ai.vercel.app
```

### 3. Create Initial Data

```bash
# Send test events to production
curl -X POST https://ops-assist-ai-backend.up.railway.app/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "service": "production-api",
    "level": "ERROR",
    "message": "Test error message"
  }'
```

---

## 🎯 Alternative Deployment Options

### Option 1: Render (Similar to Railway)

**Backend:**
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Configure:
   - **Root Directory**: `apps/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

### Option 2: Fly.io (Global Edge Deployment)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy backend
cd apps/backend
fly launch
fly deploy
```

### Option 3: AWS (Full Control)

**Backend (AWS ECS):**
```dockerfile
# Create Dockerfile in apps/backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend (AWS Amplify):**
- Connect GitHub repo
- Set root directory to `apps/frontend`
- Auto-deploys on push

---

## 🔒 Security Best Practices

### 1. Environment Variables
Never commit:
- Database passwords
- API keys
- Secret tokens

### 2. Use Secrets Management
```bash
# Railway/Vercel will encrypt these
DATABASE_URL=***
OPENAI_API_KEY=***
```

### 3. Enable HTTPS
All platforms provide free SSL certificates automatically.

### 4. Rate Limiting (Add Later)
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/events")
@limiter.limit("100/minute")
async def create_event(...):
    ...
```

---

## 📊 Monitoring & Logging

### 1. Railway Logs
```bash
# View logs
railway logs

# Or in dashboard
https://railway.app/project/[PROJECT_ID]/logs
```

### 2. Vercel Logs
Dashboard → Deployments → Select deployment → Logs

### 3. Supabase Monitoring
Dashboard → Reports → Database performance

### 4. Add Error Tracking (Optional)
```bash
# Add Sentry
pip install sentry-sdk

# In main.py
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

---

## 🚀 Continuous Deployment

### Automatic Deployment on Push

Both Railway and Vercel automatically deploy when you push to GitHub:

```bash
git add .
git commit -m "feat: new feature"
git push origin main

# Railway redeploys backend
# Vercel redeploys frontend
# Both complete in ~2-3 minutes
```

### Branch Previews

Vercel creates preview URLs for every branch:
```bash
git checkout -b feature/new-feature
git push origin feature/new-feature

# Vercel creates: https://ops-assist-ai-git-feature-new-feature.vercel.app
```

---

## 💰 Cost Estimate

### Free Tier (Learning/MVP)
- **Frontend (Vercel)**: $0/month
- **Backend (Railway)**: $5 credit (lasts 1-2 months)
- **Database (Supabase)**: $0/month
- **Total**: ~$0-3/month

### Production (100-1000 users)
- **Frontend (Vercel Pro)**: $20/month
- **Backend (Railway)**: $10-30/month
- **Database (Supabase Pro)**: $25/month
- **Total**: ~$55-75/month

### Scale (1000+ users)
- **Frontend (Vercel Pro)**: $20/month
- **Backend (Railway/AWS)**: $50-200/month
- **Database (Supabase/RDS)**: $50-200/month
- **Total**: ~$120-420/month

---

## 🔄 Update Deployment

### Update Backend
```bash
git add apps/backend
git commit -m "fix: update backend logic"
git push origin main
# Railway auto-deploys in ~2 min
```

### Update Frontend
```bash
git add apps/frontend
git commit -m "feat: new UI component"
git push origin main
# Vercel auto-deploys in ~1 min
```

### Database Migrations
```bash
# Create migration
cd apps/backend
alembic revision --autogenerate -m "add new column"

# Apply to production (be careful!)
alembic upgrade head
```

---

## 🎓 Quick Start Checklist

- [ ] Create Supabase account and database
- [ ] Get database connection string
- [ ] Create Railway account
- [ ] Deploy backend to Railway
- [ ] Add environment variables to Railway
- [ ] Get Railway backend URL
- [ ] Create Vercel account
- [ ] Update CORS in backend with Vercel domain
- [ ] Deploy frontend to Vercel
- [ ] Add environment variables to Vercel
- [ ] Test production deployment
- [ ] Share URL with users!

---

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check Railway logs
railway logs

# Common issues:
# - Missing environment variable
# - Database connection failed
# - Port binding error
```

### Frontend can't connect to backend
```bash
# Check CORS settings
# Verify NEXT_PUBLIC_API_URL is correct
# Check Railway backend logs for requests
```

### Database connection errors
```bash
# Verify DATABASE_URL format
# Check Supabase project is active
# Test connection with psql
psql "postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
```

---

## 📚 Additional Resources

- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

---

## 🎯 Next Steps After Deployment

1. **Custom Domain** - Add your own domain (e.g., ops-assist.yourdomain.com)
2. **Authentication** - Add user login with Auth0 or Supabase Auth
3. **Monitoring** - Set up Sentry or LogRocket
4. **Analytics** - Add Google Analytics or PostHog
5. **Backups** - Enable automatic database backups
6. **CI/CD** - Add GitHub Actions for automated testing
7. **Documentation** - Create API documentation site

---

## 🚀 Your Deployed URLs

Once deployed, you'll have:

```
Frontend:  https://ops-assist-ai.vercel.app
Backend:   https://ops-assist-ai-backend.up.railway.app
API Docs:  https://ops-assist-ai-backend.up.railway.app/docs
Database:  [Supabase Dashboard]
```

Share the frontend URL with anyone - no setup required! 🎉
