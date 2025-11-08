# Environment Variables Summary

## Current Environment Variables

### Backend (.env)
Located at: `backend/.env`
```
✅ SUPABASE_URL=https://tedxbpbzcxogwijcqjbj.supabase.co
✅ SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
✅ SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
✅ PORT=5000
```

### Data Pipeline (.env)
Located at: `data_pipeline/.env`
```
✅ NCBI_API_KEY=596a870f5e014c29126394af437150acbf08
✅ SUPABASE_URL=https://tedxbpbzcxogwijcqjbj.supabase.co
✅ SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
✅ PUBMED_DEFAULT_QUERY=radiation oncology
```

### ML Service
❌ No .env file found in `ml_service/`

---

## Required Environment Variables by Service

### Backend Service
**Currently Set:**
- ✅ SUPABASE_URL
- ✅ SUPABASE_ANON_KEY
- ✅ SUPABASE_SERVICE_KEY
- ✅ PORT (set to 5000, but backend typically uses 3000)

**Missing/Using Defaults:**
- ⚠️ NODE_ENV (defaults to 'development')
- ⚠️ MONGODB_URI (defaults to 'mongodb://localhost:27017/health_ai')
- ⚠️ JWT_SECRET (defaults to 'your-secret-key-change-in-production' - **INSECURE**)
- ⚠️ JWT_EXPIRE (defaults to '7d')
- ⚠️ FRONTEND_URL (defaults to 'http://localhost:3001')
- ⚠️ ML_SERVICE_URL (defaults to 'http://localhost:5000')
- ⚠️ RATE_LIMIT_WINDOW_MS (defaults to 900000)
- ⚠️ RATE_LIMIT_MAX (defaults to 100)
- ⚠️ LOG_LEVEL (defaults to 'info')

**⚠️ CRITICAL: JWT_SECRET should be set to a secure random string in production!**

### ML Service
**Currently Set:**
- None (no .env file)

**Missing/Using Defaults:**
- ⚠️ RETRIEVER_MODEL (defaults to 'sentence-transformers/all-MiniLM-L6-v2')
- ⚠️ RERANKER_MODEL (defaults to 'cross-encoder/ms-marco-MiniLM-L-6-v2')
- ⚠️ SUMMARIZER_MODEL (defaults to 'facebook/bart-large-cnn')
- ⚠️ NLI_MODEL (defaults to 'microsoft/deberta-v3-base')
- ⚠️ HYBRID_ALPHA (defaults to '0.5')
- ⚠️ DEFAULT_LIMIT (defaults to '10')
- ⚠️ SUMMARY_MAX_LENGTH (defaults to '150')
- ⚠️ SUMMARY_MIN_LENGTH (defaults to '30')
- ⚠️ HOST (defaults to '0.0.0.0')
- ⚠️ PORT (defaults to '5000')
- ⚠️ ALLOWED_ORIGINS (defaults to 'http://localhost:3000,http://localhost:3001')

### Data Pipeline
**Currently Set:**
- ✅ NCBI_API_KEY
- ✅ SUPABASE_URL
- ✅ SUPABASE_SERVICE_KEY
- ✅ PUBMED_DEFAULT_QUERY

**All required variables are set! ✅**

### Docker Compose
**Environment Variables Referenced:**
- FRONTEND_PORT (defaults to 3001)
- REACT_APP_API_URL (defaults to http://localhost:3000)
- BACKEND_PORT (defaults to 3000)
- BACKEND_ENV (defaults to development)
- DATABASE_URL (required for backend and airflow)
- REDIS_URL (required for backend)
- JWT_SECRET (required for backend)
- ML_SERVICE_PORT (defaults to 5000)
- ML_SERVICE_ENV (defaults to development)
- OPENAI_API_KEY (optional, for ML service)
- ANTHROPIC_API_KEY (optional, for ML service)
- AIRFLOW_URL (defaults to 8080)
- POSTGRES_USER (defaults to user)
- POSTGRES_PASSWORD (defaults to password)
- POSTGRES_DB (defaults to health_ai)

---

## Recommendations

### High Priority
1. **Add JWT_SECRET to backend/.env** - Critical for security
   ```bash
   JWT_SECRET=<generate-a-secure-random-string>
   ```

2. **Add MONGODB_URI to backend/.env** if using MongoDB
   ```bash
   MONGODB_URI=mongodb://localhost:27017/health_ai
   ```

3. **Create ml_service/.env** with at least:
   ```bash
   PORT=5000
   HOST=0.0.0.0
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
   ```

### Medium Priority
4. **Add NODE_ENV to backend/.env** for production
   ```bash
   NODE_ENV=production
   ```

5. **Add FRONTEND_URL to backend/.env** if frontend is on different domain
   ```bash
   FRONTEND_URL=http://localhost:3001
   ```

6. **Add ML_SERVICE_URL to backend/.env** if ML service is on different host/port
   ```bash
   ML_SERVICE_URL=http://localhost:5000
   ```

### Optional
7. **Add LOG_LEVEL to backend/.env** for better logging control
   ```bash
   LOG_LEVEL=info
   ```

8. **Add rate limiting configs** if you want to customize
   ```bash
   RATE_LIMIT_WINDOW_MS=900000
   RATE_LIMIT_MAX=100
   ```

---

## Notes
- The backend PORT is set to 5000 in .env, but the code defaults to 3000. This might cause confusion.
- All Supabase credentials are properly configured ✅
- Data pipeline has all required variables ✅
- ML service needs a .env file created

