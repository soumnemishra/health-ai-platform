"""
Configuration parser and manager
"""
import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def load_config(config_path: str = "configs/config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded config from {config_path}")
        return config
    except FileNotFoundError:
        logger.warning(f"Config file not found: {config_path}, using defaults")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Get default configuration"""
    return {
        "models": {
            "retriever": os.getenv("RETRIEVER_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
            "reranker": os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"),
            "summarizer": os.getenv("SUMMARIZER_MODEL", "facebook/bart-large-cnn"),
            "nli": os.getenv("NLI_MODEL", "microsoft/deberta-v3-base")
        },
        "retrieval": {
            "hybrid_alpha": float(os.getenv("HYBRID_ALPHA", "0.5")),
            "default_limit": int(os.getenv("DEFAULT_LIMIT", "10"))
        },
        "summarization": {
            "max_length": int(os.getenv("SUMMARY_MAX_LENGTH", "150")),
            "min_length": int(os.getenv("SUMMARY_MIN_LENGTH", "30"))
        },
        "server": {
            "host": os.getenv("HOST", "0.0.0.0"),
            "port": int(os.getenv("PORT", "5000"))
        }
    }

