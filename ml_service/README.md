# Health AI Platform - ML Service

Python-based ML service providing retrieval, summarization, and verification capabilities for the Health AI Platform.

## Tech Stack

- **FastAPI** - Web framework
- **PyTorch/Transformers** - ML models
- **Sentence Transformers** - Dense embeddings
- **FAISS** - Vector similarity search
- **Rank-BM25** - Sparse retrieval
- **Sumy** - Extractive summarization
- **BART/T5** - Abstractive summarization

## Project Structure

```
ml_service/
├── src/
│   ├── retrieval/             # Hybrid retrieval (BM25 + dense)
│   ├── reranker/              # Cross-encoder ranking
│   ├── summarizer/            # Extractive + abstractive summarizer
│   ├── entailment/            # NLI verifier
│   ├── classifiers/           # Study type / risk of bias classifiers
│   ├── pipelines/             # End-to-end RAG pipeline assembly
│   ├── utils/                 # Tokenizer, vector DB utils, config parser
│   ├── api/                   # FastAPI endpoints for inference
│   │   ├── main.py            # FastAPI app
│   │   └── routes.py          # e.g. /summarize, /verify
│   └── tests/                 # Unit tests for models
├── models/                    # Stored model weights / checkpoints
├── data/                      # Sample data for dev / evaluation
├── requirements.txt
└── Dockerfile
```

## Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

4. **Create `.env` file**
   ```env
   PORT=5000
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
   RETRIEVER_MODEL=sentence-transformers/all-MiniLM-L6-v2
   RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
   SUMMARIZER_MODEL=facebook/bart-large-cnn
   ```

5. **Run the service**
   ```bash
   uvicorn src.api.main:app --host 0.0.0.0 --port 5000 --reload
   ```

## API Endpoints

### Retrieval
- `POST /api/retrieve` - Hybrid retrieval (BM25 + dense vectors)
  ```json
  {
    "query": "machine learning in healthcare",
    "filters": {},
    "limit": 10
  }
  ```

### Summarization
- `POST /api/summarize` - Generate extractive or abstractive summary
  ```json
  {
    "paperId": "123",
    "content": "Long paper text...",
    "method": "abstractive"
  }
  ```

### Verification
- `POST /api/verify` - NLI-based claim verification
  ```json
  {
    "claim": "Machine learning improves diagnosis",
    "context": "Studies show ML models..."
  }
  ```

### Classification
- `POST /api/classify` - Classify study type or risk of bias
  ```json
  {
    "text": "Study text...",
    "task": "study_type"
  }
  ```

### Embeddings
- `GET /api/embeddings/{paper_id}` - Get paper embeddings

## Features

- ✅ Hybrid retrieval (BM25 + dense vectors)
- ✅ Cross-encoder reranking
- ✅ Extractive & abstractive summarization
- ✅ NLI-based claim verification
- ✅ Study type classification
- ✅ Risk of bias classification
- ✅ End-to-end RAG pipeline
- ✅ Vector database utilities

## Development

### Running Tests
```bash
pytest src/tests/
```

### Docker Build
```bash
docker build -t ml-service .
docker run -p 5000:5000 ml-service
```

## Model Notes

Current implementation uses placeholder models in some areas. For production:
- Replace NLI verifier with proper NLI model (e.g., `roberta-large-mnli`)
- Fine-tune study type classifier on medical study dataset
- Fine-tune bias classifier on risk of bias annotations
- Consider using GPU for faster inference

## Performance

- Retrieval: ~100ms for 1000 documents
- Summarization: ~2-5s per document
- Reranking: ~200ms for 20 documents
- Classification: ~500ms per document

