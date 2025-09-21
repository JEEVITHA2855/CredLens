import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RAW_DATA_DIR = DATA_DIR / "raw"

# Database
DATABASE_URL = str(DATA_DIR / "credlens.db")

# AI Models
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Using full HF model ID
NLI_MODEL = "facebook/bart-large-mnli"
FAISS_INDEX_PATH = str(PROCESSED_DATA_DIR / "faiss_index")
EMBEDDINGS_PATH = str(PROCESSED_DATA_DIR / "embeddings.npy")

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8000
DEBUG = True

# Credibility thresholds
CREDIBILITY_THRESHOLDS = {
    "high": 0.8,
    "medium": 0.5,
    "low": 0.3
}

# Suspicious words for sensational text detection
SUSPICIOUS_WORDS = [
    "shocking", "unbelievable", "incredible", "amazing", "breaking", 
    "urgent", "must see", "revealed", "exposed", "secret", "hidden",
    "they don't want you to know", "mainstream media", "cover-up",
    "conspiracy", "hoax", "fake news", "lies", "deception",
    "exclusive", "insider", "leaked", "bombshell"
]

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(RAW_DATA_DIR, exist_ok=True)