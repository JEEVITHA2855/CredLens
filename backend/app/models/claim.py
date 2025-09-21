from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum

class VerificationStatus(str, Enum):
    TRUE = "TRUE"  # Strong supporting evidence, no major contradictions
    FALSE = "FALSE"  # Strong contradicting evidence, no credible support
    AMBIGUOUS = "AMBIGUOUS"  # Evidence is mixed, insufficient, or context-dependent
    
    @classmethod
    def _missing_(cls, value):
        """Handle missing values by mapping them to AMBIGUOUS"""
        if isinstance(value, str):
            value_upper = value.upper()
            if value_upper == "MIXED":
                return cls.AMBIGUOUS
            elif value_upper == "LIKELY_FALSE":
                return cls.FALSE
            elif value_upper == "LIKELY_TRUE":
                return cls.TRUE
        return cls.AMBIGUOUS

class ClaimInput(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

class CredibilityFingerprint(BaseModel):
    overall_credibility: float = Field(..., ge=0, le=100, description="Overall credibility score (0-100%)")
    source_trust: float = Field(..., ge=0, le=100, description="Source trustworthiness score (0-100%)")
    corroboration_count: int = Field(..., ge=0, description="Number of supporting sources")
    contradiction_count: int = Field(..., ge=0, description="Number of contradicting sources")
    language_safety: float = Field(..., ge=0, le=100, description="Language safety score (0-100%)")

class Evidence(BaseModel):
    text: str
    source: str
    url: Optional[str] = None
    type: str = Field(..., description="Type of evidence: SUPPORT, CONTRADICT, or CONTEXT")
    reliability_score: float = Field(..., ge=0, le=100, description="Source reliability score (0-100%)")
    date: Optional[str] = None  # Date of the evidence if available
    region: Optional[str] = None  # Geographic region if relevant
    verification_method: str = Field(..., description="How the evidence was verified (e.g., peer-review, fact-check, news)")

class SuspiciousPhrase(BaseModel):
    phrase: str
    start_pos: int
    end_pos: int
    reason: str

class MicroLesson(BaseModel):
    tip: str
    category: str  # e.g., "source_verification", "language_analysis", "cross_referencing"

class ClaimAnalysis(BaseModel):
    original_input: Optional[str] = None
    extracted_claim: Optional[str] = None
    verification_status: VerificationStatus
    credibility_fingerprint: Dict[str, float]
    evidence: List[Dict[str, Any]]
    suspicious_phrases: List[str] = []
    micro_lesson: Optional[Dict[str, str]] = None
    explanation: str
    
    # Add custom validation to ensure verification_status is correct
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