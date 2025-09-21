"""
FastAPI endpoints for cloud-based misinformation detection.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.cloud_fact_checker import CloudFactChecker
from app.config import settings

router = APIRouter()

# Initialize cloud fact checker
fact_checker = CloudFactChecker(
    project_id=settings.GOOGLE_CLOUD_PROJECT,
    location=settings.GOOGLE_CLOUD_LOCATION,
    model_name=settings.MODEL_NAME
)

class ClaimRequest(BaseModel):
    text: str
    context: Optional[Dict[str, Any]] = None

class BatchClaimRequest(BaseModel):
    claims: List[str]

@router.post("/analyze-claim")
async def analyze_claim(request: ClaimRequest):
    """Analyze a single claim for misinformation."""
    try:
        result = fact_checker.analyze_claim(request.text)
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-batch")
async def analyze_batch(request: BatchClaimRequest):
    """Analyze multiple claims in batch."""
    try:
        results = fact_checker.batch_analyze_claims(request.claims)
        return {
            "status": "success",
            "data": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-metrics")
async def get_model_metrics():
    """Get current model performance metrics."""
    try:
        metrics = fact_checker.get_model_metrics()
        return {
            "status": "success",
            "data": metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain-prediction")
async def explain_prediction(request: ClaimRequest):
    """Get detailed explanation for a prediction."""
    try:
        explanation = fact_checker.get_explanation(request.text)
        return {
            "status": "success",
            "data": explanation,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))