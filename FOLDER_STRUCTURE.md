# Health AI Platform - Complete Folder Structure

## Project Overview
This is a full-stack health AI platform with backend API, frontend UI, ML service, and data pipeline components.

---

## Root Directory Structure

```
health-ai-platform/
├── backend/                    # Node.js/Express Backend API
├── frontend/                   # React/Vite Frontend Application
├── ml_service/                 # Python ML/AI Service (FastAPI)
├── data_pipeline/              # Airflow Data Pipeline
├── docker/                     # Docker configurations
├── configs/                    # Shared configuration files
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
├── tests/                      # Integration tests
├── docker-compose.yml          # Docker Compose configuration
├── package.json                # Root package.json (monorepo)
├── package-lock.json           # NPM lock file
├── README.md                   # Project README
├── project_over_view.txt       # Project overview document
└── .gitignore                  # Git ignore rules
```

---

## Backend Structure (`backend/`)

```
backend/
├── src/
│   ├── api/
│   │   ├── controllers/        # Request handlers (business logic)
│   │   │   ├── auth.controller.js
│   │   │   ├── user.controller.js
│   │   │   ├── paper.controller.js
│   │   │   └── alert.controller.js
│   │   ├── middleware/         # Express middleware
│   │   │   ├── auth.middleware.js
│   │   │   └── validation.middleware.js
│   │   ├── routes/             # API route definitions
│   │   │   ├── auth.routes.js
│   │   │   ├── user.routes.js
│   │   │   ├── paper.routes.js
│   │   │   ├── alert.routes.js
│   │   │   └── articles.js     # Supabase articles route
│   │   └── validators/         # Input validation schemas
│   │       ├── auth.validator.js
│   │       └── paper.validator.js
│   ├── config/                 # Configuration files
│   │   └── index.js
│   ├── db/                     # Database connections
│   │   ├── connection.js       # MongoDB connection
│   │   └── supabase.js         # Supabase client
│   ├── models/                 # Database models (Mongoose)
│   │   ├── User.model.js
│   │   ├── Paper.model.js
│   │   ├── Alert.model.js
│   │   └── Feedback.model.js
│   ├── services/               # Business logic services
│   │   ├── retrieval.service.js
│   │   └── summaryCache.service.js
│   ├── utils/                  # Utility functions
│   │   ├── logger.js
│   │   ├── errorHandler.js
│   │   └── scoringUtils.js
│   ├── jobs/                   # Scheduled jobs (cron)
│   │   ├── dailyDigest.job.js
│   │   └── cleanup.job.js
│   ├── app.js                  # Express app configuration
│   └── server.js               # Server entry point
├── tests/                      # Backend tests
│   ├── auth.test.js
│   └── setup.js
├── logs/                       # Application logs
│   ├── combined.log
│   └── error.log
├── jest.config.js              # Jest test configuration
├── package.json                # Backend dependencies
└── README.md                   # Backend documentation
```

**Key Backend Files:**
- `server.js` - Application entry point, starts Express server
- `app.js` - Express app setup, middleware, routes
- `db/connection.js` - MongoDB connection (optional)
- `db/supabase.js` - Supabase client (lazy initialization)
- `api/routes/articles.js` - Articles API endpoint (reads from Supabase)

---

## Frontend Structure (`frontend/`)

```
frontend/
├── src/
│   ├── api/                    # API client configuration
│   │   └── client.js
│   ├── components/             # Reusable React components
│   │   ├── NavBar.jsx
│   │   ├── Card.jsx
│   │   └── Loader.jsx
│   ├── context/                # React Context providers
│   │   ├── UserContext.jsx
│   │   └── ThemeContext.jsx
│   ├── features/               # Feature components
│   │   ├── Feed.jsx
│   │   ├── PaperDetail.jsx
│   │   └── Alerts.jsx
│   ├── hooks/                  # Custom React hooks
│   │   ├── useAuth.js
│   │   └── useFetch.js
│   ├── pages/                  # Page components
│   │   ├── Home.jsx
│   │   ├── Dashboard.jsx
│   │   └── Login.jsx
│   ├── routes/                 # Routing configuration
│   │   └── AppRoutes.jsx
│   ├── styles/                 # Global styles
│   │   └── index.css
│   ├── utils/                  # Utility functions
│   │   ├── formatDate.js
│   │   └── scoreColors.js
│   ├── assets/                 # Static assets (images, etc.)
│   ├── App.jsx                 # Main App component
│   └── main.jsx               # Application entry point
├── index.html                  # HTML template
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── postcss.config.js           # PostCSS configuration
├── package.json                # Frontend dependencies
└── README.md                   # Frontend documentation
```

---

## ML Service Structure (`ml_service/`)

```
ml_service/
├── src/
│   ├── api/                    # FastAPI application
│   │   ├── main.py             # FastAPI app entry point
│   │   └── routes.py           # API route handlers
│   ├── pipelines/              # ML pipelines
│   │   └── rag_pipeline.py     # RAG (Retrieval-Augmented Generation)
│   ├── retrieval/              # Document retrieval
│   │   └── hybrid_retriever.py
│   ├── reranker/               # Result reranking
│   │   └── cross_encoder.py
│   ├── summarizer/             # Text summarization
│   │   ├── extractive_summarizer.py
│   │   └── abstractive_summarizer.py
│   ├── entailment/             # Natural Language Inference
│   │   └── nli_verifier.py
│   ├── classifiers/            # Classification models
│   │   ├── study_classifier.py
│   │   └── bias_classifier.py
│   ├── utils/                  # Utility functions
│   │   ├── config.py
│   │   ├── tokenizer.py
│   │   └── vector_db.py
│   └── tests/                  # ML service tests
│       ├── test_retrieval.py
│       └── test_summarizer.py
├── data/                       # Data storage
├── models/                     # Trained ML models
├── venv/                       # Python virtual environment
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
└── README.md                   # ML service documentation
```

---

## Data Pipeline Structure (`data_pipeline/`)

```
data_pipeline/
├── dags/                       # Airflow DAGs
│   ├── ingest_pubmed.py        # PubMed data ingestion
│   ├── process_papers.py       # Paper processing
│   ├── sync_openalex.py        # OpenAlex synchronization
│   └── index_to_faiss.py      # FAISS indexing
├── scripts/                    # Data processing scripts
│   ├── pubmed_ingester.py
│   ├── paper_processor.py
│   ├── openalex_syncer.py
│   ├── data_cleaner.py
│   └── faiss_indexer.py
├── configs/                    # Configuration files
│   ├── pipeline_config.yaml
│   ├── sources_config.yaml
│   └── thresholds_config.yaml
├── notebooks/                  # Jupyter notebooks
│   └── exploratory_analysis.ipynb
├── requirements.txt            # Python dependencies
└── README.md                   # Pipeline documentation
```

---

## Environment Variables

### Backend (`backend/.env`)
```
# Server
PORT=3000
NODE_ENV=development
FRONTEND_URL=http://localhost:3001

# Database (Optional - MongoDB)
MONGO_URI=mongodb://localhost:27017/health_ai
MONGODB_URI=mongodb://localhost:27017/health_ai

# Supabase (Required for articles API)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_ANON_KEY=your-anon-key

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRE=7d

# ML Service
ML_SERVICE_URL=http://localhost:5000

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX=100
```

### ML Service (`ml_service/.env`)
```
# API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# Model Configuration
MODEL_PATH=./models
VECTOR_DB_PATH=./data/vector_db

# Supabase (for data access)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
```

---

## Key Technologies

### Backend
- **Runtime:** Node.js (ES Modules)
- **Framework:** Express.js
- **Database:** MongoDB (Mongoose) + Supabase
- **Authentication:** JWT (jsonwebtoken)
- **Validation:** Joi
- **Logging:** Winston
- **Testing:** Jest

### Frontend
- **Framework:** React
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **State Management:** React Context API
- **Routing:** React Router

### ML Service
- **Framework:** FastAPI
- **ML Libraries:** Transformers, PyTorch, FAISS
- **NLP:** spaCy, NLTK, Sumy
- **Vector DB:** FAISS

### Data Pipeline
- **Orchestration:** Apache Airflow
- **Data Sources:** PubMed, OpenAlex
- **Processing:** Python scripts

---

## API Endpoints

### Backend API (`/api/*`)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user
- `GET /api/users` - Get all users (admin)
- `GET /api/users/:id` - Get user by ID
- `GET /api/papers` - Get all papers
- `GET /api/papers/search` - Search papers
- `GET /api/papers/:id` - Get paper by ID
- `GET /api/alerts` - Get user alerts
- `GET /api/articles` - Get articles from Supabase

---

## Database Schema

### MongoDB Collections (via Mongoose)
- **Users** - User accounts and profiles
- **Papers** - Research papers metadata
- **Alerts** - User alert subscriptions
- **Feedback** - User feedback

### Supabase Tables
- **raw_articles** - Raw article data from data pipeline

---

## Development Workflow

1. **Backend Development:**
   ```bash
   cd backend
   npm install
   npm run dev
   ```

2. **Frontend Development:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **ML Service:**
   ```bash
   cd ml_service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn src.api.main:app --reload
   ```

4. **Data Pipeline:**
   ```bash
   cd data_pipeline
   # Setup Airflow environment
   # Run DAGs via Airflow UI
   ```

---

## Deployment

- **Docker Compose:** Use `docker-compose.yml` for local development
- **Production:** Deploy each service independently
  - Backend: Node.js server (PM2, Docker)
  - Frontend: Static build (Nginx, Vercel, Netlify)
  - ML Service: FastAPI (Docker, Kubernetes)
  - Data Pipeline: Airflow (Docker, Cloud Composer)

---

## Notes

- MongoDB connection is **optional** - app works with Supabase only
- Supabase client uses **lazy initialization** - only connects when needed
- All services can run independently
- Environment variables should be set per service
- Logs are stored in `backend/logs/` directory

---

*Last Updated: 2025-11-04*
