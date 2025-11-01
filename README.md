# Health AI Platform

A comprehensive multi-service architecture for healthcare AI applications, featuring retrieval-augmented generation (RAG), document summarization, and intelligent health data processing.

## Architecture Overview

This platform consists of four main services:

- **Frontend**: React-based user interface
- **Backend**: Node.js/Express API server
- **ML Service**: Python-based ML pipelines for retrieval and summarization
- **Data Pipeline**: Airflow/Prefect jobs for data ingestion and indexing

## Project Structure

```
health_ai_platform/
├── frontend/                 # React app (UI)
├── backend/                  # Node.js/Express server (API layer)
├── ml_service/               # Python-based ML pipelines (retrieval, summarization)
├── data_pipeline/            # Airflow/Prefect jobs for ingestion + indexing
├── configs/                  # Config YAMLs/JSON for all environments
├── scripts/                  # DevOps / setup scripts
├── docker/                   # Dockerfiles for each service
├── tests/                    # Integration / e2e tests
├── docs/                     # API docs, architecture, notes
├── .env                      # Environment variables
├── docker-compose.yml        # Local multi-service setup
├── package.json              # Root dependencies (if shared)
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local ML service development)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd health_ai_platform
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the services**
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:3000
   - ML Service: http://localhost:5000
   - Airflow UI: http://localhost:8080

## Development

### Local Development Setup

Each service can be run independently for development:

- **Frontend**: See `frontend/README.md`
- **Backend**: See `backend/README.md`
- **ML Service**: See `ml_service/README.md`
- **Data Pipeline**: See `data_pipeline/README.md`

### Running Tests

```bash
npm test
```

## Configuration

Environment-specific configurations are stored in the `configs/` directory. Each service can have its own configuration files for different environments (development, staging, production).

## Documentation

- API Documentation: `docs/api/`
- Architecture Notes: `docs/architecture/`
- Setup Guides: `docs/setup/`

## Contributing

Please read the contributing guidelines before submitting pull requests.

## License

MIT

