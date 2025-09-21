"""
Simple CredLens Backend Server
Bypasses problematic Google Cloud ML imports and uses only working components
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import hashlib
from typing import Optional, Dict, List, Any
import os
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import only the working components
from app.models.claim import ClaimInput, ClaimAnalysis, VerificationStatus, CredibilityFingerprint
from app.services.enhanced_fact_checker import EnhancedFactChecker

# Import your working Gemini fact checker from demo
sys.path.append(str(Path(__file__).parent / "demo"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize only the working services
enhanced_fact_checker = None

app = FastAPI(
    title="CredLens API",
    description="AI-powered misinformation detection and education tool",
    version="1.0.0"
)

# Add CORS middleware for both ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "http://localhost:3001", 
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    message: str

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global enhanced_fact_checker
    
    try:
        print("Initializing Enhanced Fact Checker...")
        enhanced_fact_checker = EnhancedFactChecker()
        print("✅ CredLens Simple API started successfully!")
    except Exception as e:
        print(f"⚠️ Warning during startup: {e}")
        # Continue without the problematic service

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
    """Analyze a claim for misinformation using available services"""
    try:
        # Validate input
        if not claim_input.text and not claim_input.url:
            raise HTTPException(status_code=400, detail="Either text or URL must be provided")
        
        text_to_analyze = claim_input.text or claim_input.url
        
        print(f"📝 Analyzing claim: {text_to_analyze[:100]}...")
        
        # Use the Enhanced Fact Checker if available
        if enhanced_fact_checker:
            try:
                result = enhanced_fact_checker.verify_claim(text_to_analyze)
                print(f"✅ Enhanced fact checker result: {result.status}")
                return result
            except Exception as e:
                print(f"⚠️ Enhanced fact checker failed: {e}")
        
        # Fallback to Gemini-based analysis
        try:
            import google.generativeai as genai
            
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise Exception("GEMINI_API_KEY not found")
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""Analyze this claim for misinformation: "{text_to_analyze}"
            
            Respond with a JSON object containing:
            {{
                "verdict": "TRUE" | "FALSE" | "AMBIGUOUS",
                "confidence": <0-100>,
                "explanation": "<detailed reasoning>",
                "sources": ["<source1>", "<source2>"]
            }}
            
            Use current information and be thorough in your analysis."""
            
            response = model.generate_content(prompt)
            response_text = response.text
            
            # Try to extract JSON
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end != 0:
                    json_text = response_text[json_start:json_end]
                    gemini_result = json.loads(json_text)
                    
                    # Convert to our format
                    status_map = {
                        'TRUE': VerificationStatus.VERIFIED,
                        'FALSE': VerificationStatus.DEBUNKED,
                        'AMBIGUOUS': VerificationStatus.UNCERTAIN
                    }
                    
                    status = status_map.get(gemini_result.get('verdict', 'AMBIGUOUS'), VerificationStatus.UNCERTAIN)
                    confidence = gemini_result.get('confidence', 50) / 100.0
                    
                    fingerprint = CredibilityFingerprint(
                        factual_accuracy=confidence,
                        source_reliability=confidence,
                        claim_consistency=confidence,
                        evidence_quality=confidence,
                        overall_credibility=confidence
                    )
                    
                    result = ClaimAnalysis(
                        claim_text=text_to_analyze,
                        status=status,
                        confidence_score=confidence,
                        explanation=gemini_result.get('explanation', 'Analysis completed using Gemini AI'),
                        evidence=gemini_result.get('sources', []),
                        credibility_fingerprint=fingerprint,
                        metadata={
                            "analysis_method": "gemini_fallback",
                            "model": "gemini-1.5-flash",
                            "timestamp": str(hash(text_to_analyze) % 10000)
                        }
                    )
                    
                    print(f"✅ Gemini analysis result: {status}")
                    return result
                    
            except json.JSONDecodeError:
                pass
                
        except Exception as e:
            print(f"⚠️ Gemini analysis failed: {e}")
        
        # Ultimate fallback
        print("⚠️ Using basic fallback analysis")
        
        # Simple keyword-based analysis as last resort
        suspicious_keywords = ['always', 'never', 'everyone knows', 'scientists say', 'doctors hate', 'secret']
        suspicious_count = sum(1 for keyword in suspicious_keywords if keyword.lower() in text_to_analyze.lower())
        
        if suspicious_count >= 2:
            status = VerificationStatus.UNCERTAIN
            confidence = 0.3
            explanation = f"Claim contains {suspicious_count} suspicious phrases that often indicate misinformation."
        else:
            status = VerificationStatus.UNCERTAIN
            confidence = 0.5
            explanation = "Unable to verify this claim with available services. Please verify with reliable sources."
        
        fingerprint = CredibilityFingerprint(
            factual_accuracy=confidence,
            source_reliability=confidence,
            claim_consistency=confidence,
            evidence_quality=confidence,
            overall_credibility=confidence
        )
        
        result = ClaimAnalysis(
            claim_text=text_to_analyze,
            status=status,
            confidence_score=confidence,
            explanation=explanation,
            evidence=["Manual verification recommended"],
            credibility_fingerprint=fingerprint,
            metadata={
                "analysis_method": "basic_fallback",
                "suspicious_keywords_found": suspicious_count
            }
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)