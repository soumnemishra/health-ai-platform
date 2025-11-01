from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger

from src.pipelines.rag_pipeline import RAGPipeline
from src.summarizer.extractive_summarizer import ExtractiveSummarizer
from src.summarizer.abstractive_summarizer import AbstractiveSummarizer
from src.entailment.nli_verifier import NLIVerifier
from src.classifiers.study_classifier import StudyClassifier
from src.classifiers.bias_classifier import BiasClassifier

router = APIRouter()

# Initialize pipelines (lazy loading recommended in production)
rag_pipeline = None
extractive_summarizer = None
abstractive_summarizer = None
nli_verifier = None
study_classifier = None
bias_classifier = None


# Request/Response models
class RetrieveRequest(BaseModel):
    query: str
    filters: Optional[dict] = {}
    limit: int = 10


class RetrieveResponse(BaseModel):
    papers: List[dict]
    scores: List[float]


class SummarizeRequest(BaseModel):
    paperId: str
    content: str
    method: Optional[str] = "abstractive"  # "extractive" or "abstractive"


class SummarizeResponse(BaseModel):
    summary: str
    method: str


class VerifyRequest(BaseModel):
    claim: str
    context: str


class VerifyResponse(BaseModel):
    entailment: str  # "entailment", "contradiction", "neutral"
    confidence: float


class ClassifyRequest(BaseModel):
    text: str
    task: str  # "study_type" or "risk_of_bias"


class ClassifyResponse(BaseModel):
    label: str
    confidence: float


@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_papers(request: RetrieveRequest):
    """Hybrid retrieval (BM25 + dense vectors)"""
    try:
        global rag_pipeline
        if rag_pipeline is None:
            rag_pipeline = RAGPipeline()
        
        results = await rag_pipeline.retrieve(
            query=request.query,
            filters=request.filters,
            limit=request.limit
        )
        
        return RetrieveResponse(
            papers=[r["paper"] for r in results],
            scores=[r["score"] for r in results]
        )
    except Exception as e:
        logger.error(f"Retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_paper(request: SummarizeRequest):
    """Generate extractive or abstractive summary"""
    try:
        if request.method == "extractive":
            global extractive_summarizer
            if extractive_summarizer is None:
                extractive_summarizer = ExtractiveSummarizer()
            summary = await extractive_summarizer.summarize(request.content)
        else:
            global abstractive_summarizer
            if abstractive_summarizer is None:
                abstractive_summarizer = AbstractiveSummarizer()
            summary = await abstractive_summarizer.summarize(request.content)
        
        return SummarizeResponse(
            summary=summary,
            method=request.method
        )
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify", response_model=VerifyResponse)
async def verify_entailment(request: VerifyRequest):
    """NLI-based claim verification"""
    try:
        global nli_verifier
        if nli_verifier is None:
            nli_verifier = NLIVerifier()
        
        result = await nli_verifier.verify(
            claim=request.claim,
            context=request.context
        )
        
        return VerifyResponse(
            entailment=result["entailment"],
            confidence=result["confidence"]
        )
    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/classify", response_model=ClassifyResponse)
async def classify_text(request: ClassifyRequest):
    """Classify study type or risk of bias"""
    try:
        if request.task == "study_type":
            global study_classifier
            if study_classifier is None:
                study_classifier = StudyClassifier()
            result = await study_classifier.classify(request.text)
        elif request.task == "risk_of_bias":
            global bias_classifier
            if bias_classifier is None:
                bias_classifier = BiasClassifier()
            result = await bias_classifier.classify(request.text)
        else:
            raise HTTPException(status_code=400, detail="Invalid task. Use 'study_type' or 'risk_of_bias'")
        
        return ClassifyResponse(
            label=result["label"],
            confidence=result["confidence"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/embeddings/{paper_id}")
async def get_embeddings(paper_id: str):
    """Get paper embeddings for similarity search"""
    try:
        global rag_pipeline
        if rag_pipeline is None:
            rag_pipeline = RAGPipeline()
        
        embedding = await rag_pipeline.get_embedding(paper_id)
        return {"embedding": embedding.tolist()}
    except Exception as e:
        logger.error(f"Get embedding error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

