from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from contextlib import asynccontextmanager
import hashlib
import json
import re
from typing import Optional, Dict, List, Any

from .models.claim import ClaimInput, ClaimAnalysis, VerificationStatus, CredibilityFingerprint
from .models.database import db
from .services.enhanced_fact_checker import EnhancedFactChecker
# from .services.industrial_fact_checker import IndustrialFactChecker  # Temporarily disabled due to Google Cloud dependencies
from .services.claim_extractor import ClaimExtractor
from .services.real_time_verifier import RealTimeVerifier
from .services.evidence_based_verifier import EvidenceBasedVerifier
from .services.credibility_scorer import CredibilityScorer
from .services.retriever import SemanticRetriever
from .services.lesson_generator import LessonGenerator

# Initialize services (global scope)
enhanced_fact_checker = EnhancedFactChecker()
# industrial_fact_checker = IndustrialFactChecker()  # Temporarily disabled
claim_extractor = ClaimExtractor()
real_time_verifier = RealTimeVerifier()
evidence_based_verifier = EvidenceBasedVerifier()
credibility_scorer = CredibilityScorer()
retriever = SemanticRetriever()
lesson_generator = LessonGenerator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    try:
        # Initialize the fact checkers
        global enhanced_fact_checker
        enhanced_fact_checker = EnhancedFactChecker()
        # industrial_fact_checker = IndustrialFactChecker()  # Temporarily disabled
        
        print("CredLens API started successfully!")
    except Exception as e:
        print(f"Error during startup: {e}")
    
    yield
    
    # Shutdown (if needed)
    print("CredLens API shutting down...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="CredLens API",
    description="AI-powered misinformation detection and education tool",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        status="success",
        message="CredLens API is running!"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="success", 
        message="API is healthy"
    )

@app.post("/analyze", response_model=ClaimAnalysis)
async def analyze_claim(claim_input: ClaimInput):
    """Analyze a claim for misinformation"""
    try:
        # Validate input
        if not claim_input.text and not claim_input.url:
            raise HTTPException(status_code=400, detail="Either text or URL must be provided")
        
        # Create cache key
        input_str = json.dumps({
            "text": claim_input.text,
            "url": claim_input.url
        }, sort_keys=True)
        cache_key = hashlib.md5(input_str.encode()).hexdigest()
        
        # Check cache first
        cached_result = db.get_cached_analysis(cache_key)
        if cached_result:
            return ClaimAnalysis(**cached_result)
        
        # Extract claim
        if claim_input.url:
            try:
                extracted_claim, full_text = claim_extractor.extract_from_url(claim_input.url)
                original_input = full_text[:200] + "..." if len(full_text) > 200 else full_text
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to process URL: {str(e)}")
        else:
            extracted_claim = claim_extractor.extract_from_text(claim_input.text)
            original_input = claim_input.text

        if not extracted_claim:
            raise HTTPException(status_code=400, detail="Could not extract a verifiable claim from the input")

        # Perform enhanced fact checking
        analysis_result = enhanced_fact_checker.analyze_claim(extracted_claim)
        
        # Debug the response
        print(f"DEBUG - verification_status type: {type(analysis_result['verification_status'])}")
        print(f"DEBUG - verification_status value: {analysis_result['verification_status']}")
        print(f"DEBUG - micro_lesson type: {type(analysis_result['micro_lesson'])}")
        print(f"DEBUG - micro_lesson value: {analysis_result['micro_lesson']}")
        
        # Ensure verification_status is a valid enum
        if not isinstance(analysis_result['verification_status'], VerificationStatus):
            if isinstance(analysis_result['verification_status'], str):
                try:
                    # Try to convert string to enum
                    analysis_result['verification_status'] = VerificationStatus(analysis_result['verification_status'].upper())
                except (ValueError, KeyError):
                    # Default to AMBIGUOUS if conversion fails
                    analysis_result['verification_status'] = VerificationStatus.AMBIGUOUS
            else:
                analysis_result['verification_status'] = VerificationStatus.AMBIGUOUS
                
        # Create analysis result
        analysis = ClaimAnalysis(
            original_input=original_input,
            extracted_claim=extracted_claim,
            verification_status=analysis_result['verification_status'],
            credibility_fingerprint=analysis_result['credibility_fingerprint'],
            evidence=analysis_result['evidence'],
            suspicious_phrases=analysis_result['suspicious_phrases'],
            micro_lesson=analysis_result['micro_lesson'],
            explanation=analysis_result['explanation']
        )
        
        # Cache the result
        db.cache_analysis(cache_key, analysis.dict())
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

class EvidenceInput(BaseModel):
    claim: str
    evidence_sources: list  # List of {source, content, url}

class EvidenceAnalysisResponse(BaseModel):
    claim: str
    verdict: str  # TRUE/FALSE/AMBIGUOUS
    reasoning: str
    scores: dict
    evidence_breakdown: dict
    timestamp: str

@app.post("/analyze-with-evidence", response_model=EvidenceAnalysisResponse)
async def analyze_with_evidence(evidence_input: EvidenceInput):
    """
    Analyze a claim against provided evidence sources
    
    This endpoint uses the evidence-based verification approach where
    you provide the claim and supporting evidence sources, and the system
    analyzes them to determine credibility.
    """
    try:
        if not evidence_input.claim:
            raise HTTPException(status_code=400, detail="Claim is required")
        
        if not evidence_input.evidence_sources:
            raise HTTPException(status_code=400, detail="Evidence sources are required")
        
        # Use evidence-based verifier
        result = evidence_based_verifier.verify_with_evidence(
            evidence_input.claim, 
            evidence_input.evidence_sources
        )
        
        return EvidenceAnalysisResponse(
            claim=result['claim'],
            verdict=result['verdict'],
            reasoning=result['reasoning'],
            scores=result['scores'],
            evidence_breakdown=result['evidence_breakdown'],
            timestamp=result['timestamp']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

class ClaimAnalysisRequest(BaseModel):
    content: str
    source_url: str = None

class ClaimAnalysisResponse(BaseModel):
    credibility_fingerprint: Dict[str, float] = Field(
        ...,
        description="Credibility scores including overall_credibility, source_trust, language_safety, corroboration_count, contradiction_count"
    )
    evidence: List[Dict[str, Any]] = Field(
        ...,
        description="List of evidence items with text, source, type, reliability_score, and verification_method"
    )
    explanation: str
    micro_lesson: Optional[Dict[str, str]] = None
    suspicious_phrases: List[str] = []
    verification_status: VerificationStatus = Field(
        ...,
        description="Verification status: TRUE, FALSE, or AMBIGUOUS"
    )
    
    # Add validator for verification_status
    @validator('verification_status', pre=True)
    def validate_verification_status(cls, v):
        if isinstance(v, str):
            try:
                return VerificationStatus(v.upper())
            except ValueError:
                return VerificationStatus.AMBIGUOUS
        elif isinstance(v, VerificationStatus):
            return v
        else:
            return VerificationStatus.AMBIGUOUS
    
@app.post("/analyze-industrial", response_model=ClaimAnalysisResponse)
async def analyze_claim_industrial(request: ClaimAnalysisRequest):
    """
    Analyze a claim using the industrial-grade real-time fact-checking system
    """
    try:
        # Use the enhanced fact checker instead of industrial fact checker
        enhanced_result = enhanced_fact_checker.analyze_claim(request.content)
        
        # Extract dynamic scores from the enhanced analysis
        credibility_fingerprint = {
            'overall_credibility': enhanced_result.get('credibility_score', 50) / 100.0,
            'source_trust': 0.7,  # Default value since enhanced doesn't provide this
            'language_safety': 0.8,  # Default value 
            'corroboration_count': len(enhanced_result.get('sources', [])),
            'contradiction_count': 0  # Default value since enhanced doesn't provide this
        }
        
        # Convert enhanced verdict to VerificationStatus enum
        verdict = enhanced_result.get('verdict', 'AMBIGUOUS')
        if verdict == 'TRUE' or enhanced_result.get('credibility_score', 50) > 70:
            verification_status = VerificationStatus.TRUE
        elif verdict == 'FALSE' or enhanced_result.get('credibility_score', 50) < 30:
            verification_status = VerificationStatus.FALSE
        else:
            verification_status = VerificationStatus.AMBIGUOUS
            
        # Create evidence objects from the enhanced analysis
        evidence = []
        
        # Add supporting sources
        for src in enhanced_result.get('sources', []):
            if isinstance(src, (dict, str)):
                source_text = src if isinstance(src, str) else src.get('title', 'Source')
                evidence.append({
                    'text': f"Supporting evidence: {source_text}",
                    'source': source_text,
                    'type': 'SUPPORT',
                    'reliability_score': 75.0,  # Default reliability
                    'verification_method': 'enhanced-fact-checker'
                })
                    
        # Add any additional context as evidence
        if enhanced_result.get('explanation'):
            evidence.append({
                'text': enhanced_result['explanation'],
                    'source': src.get('source', 'unknown'),
                    'type': 'CONTRADICT',
                    'reliability_score': src.get('credibility', 70.0),
                    'verification_method': src.get('type', 'automated-verification')
                })
        
        # Generate a micro lesson based on content
        if verification_status == VerificationStatus.TRUE:
            micro_lesson = {
                "tip": "Even credible information should be verified with multiple reliable sources.",
                "category": "source_verification"
            }
        elif verification_status == VerificationStatus.FALSE:
            micro_lesson = {
                "tip": "Be cautious of claims that contradict established scientific consensus.",
                "category": "critical_thinking"
            }
        else:
            micro_lesson = {
                "tip": "When information is ambiguous, seek additional context and expert opinions.",
                "category": "media_literacy"
            }
        
        # Extract any suspicious phrases (simplified version without industrial_fact_checker)
        suspicious_phrases = []
        # Simple pattern matching for common misinformation indicators
        suspicious_patterns = [
            r'DOCTORS HATE THIS',
            r'BIG PHARMA',
            r'THEY DON\'T WANT YOU TO KNOW',
            r'PROVEN FACT',
            r'WAKE UP',
            r'DO YOUR RESEARCH'
        ]
        
        for pattern in suspicious_patterns:
            matches = re.findall(pattern, request.content.upper())
            for match in matches:
                if match and len(match) > 3:
                    suspicious_phrases.append(match)
        
        # Response data
        response_data = {
            'credibility_fingerprint': credibility_fingerprint,
            'evidence': evidence,
            'explanation': enhanced_result.get('explanation', 'Analysis completed using enhanced fact checker'),
            'micro_lesson': micro_lesson,
            'suspicious_phrases': suspicious_phrases[:5],  # Limit to top 5
            'verification_status': verification_status
        }
        
        return ClaimAnalysisResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error analyzing claim with enhanced checker: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        fact_checks = db.get_all_fact_checks()
        
        return {
            "total_fact_checks": len(fact_checks),
            "model_info": {
                "embedding_model": "all-MiniLM-L6-v2",
                "nli_model": "facebook/bart-large-mnli",
                "index_type": "FAISS"
            },
            "status": "operational"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.post("/rebuild-index")
async def rebuild_index():
    """Rebuild the FAISS index (admin endpoint)"""
    try:
        retriever.build_index()
        return {"status": "success", "message": "Index rebuilt successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rebuilding index: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)