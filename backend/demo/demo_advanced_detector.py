"""
Demo version of advanced detector with integrated scientific validation and mock evidence.
"""
import logging
from typing import Dict, List
import re
from datetime import datetime
from scientific_validator import ScientificValidator

logger = logging.getLogger(__name__)

class DemoAdvancedDetector:
    """Demo version with scientific validation and pattern-based verification."""
    
    def __init__(self):
        self.scientific_validator = ScientificValidator()
        
        # Mock evidence database for common claims
        self.evidence_db = {
            'vaccines_autism': {
                'verdict': 'FALSE',
                'confidence': 95,
                'explanation': 'Multiple large-scale scientific studies confirm no link between vaccines and autism. Health authorities worldwide have debunked this claim.',
                'sources': ['https://www.cdc.gov', 'https://www.who.int', 'https://www.nejm.org']
            },
            'earth_round': {
                'verdict': 'TRUE', 
                'confidence': 100,
                'explanation': 'The spherical shape of Earth is well-established scientific fact supported by centuries of evidence.',
                'sources': ['https://www.nasa.gov', 'https://www.britannica.com', 'https://en.wikipedia.org']
            },
            'covid_vaccines_effective': {
                'verdict': 'TRUE',
                'confidence': 90,
                'explanation': 'Clinical trials and real-world data show COVID-19 vaccines are highly effective at preventing severe illness and death.',
                'sources': ['https://www.cdc.gov', 'https://www.nejm.org', 'https://www.who.int']
            },
            '5g_coronavirus': {
                'verdict': 'FALSE',
                'confidence': 100,
                'explanation': 'There is no scientific evidence linking 5G technology to COVID-19. This conspiracy theory has been thoroughly debunked.',
                'sources': ['https://www.who.int', 'https://www.fcc.gov', 'https://www.reuters.com']
            },
            'climate_change_hoax': {
                'verdict': 'FALSE',
                'confidence': 98,
                'explanation': 'Climate change is real and primarily caused by human activities. This is supported by overwhelming scientific consensus.',
                'sources': ['https://www.nasa.gov', 'https://www.ipcc.ch', 'https://www.nature.com']
            },
            'chocolate_happiness': {
                'verdict': 'AMBIGUOUS',
                'confidence': 60,
                'explanation': 'Some studies suggest chocolate may have mood-boosting effects, but evidence is mixed and individual responses vary.',
                'sources': ['https://www.ncbi.nlm.nih.gov', 'https://www.mayoclinic.org']
            }
        }
    
    def analyze(self, input_text: str) -> Dict:
        """Main analysis pipeline with scientific validation and pattern matching."""
        try:
            # Extract primary claim
            primary_claim = input_text.strip()
            
            # First check scientific validator
            scientific_result = self.scientific_validator.validate_scientific_claim(primary_claim)
            
            if scientific_result['is_scientific']:
                return {
                    "claim": primary_claim,
                    "verdict": "TRUE",
                    "confidence": scientific_result['confidence'],
                    "sources": scientific_result['sources'],
                    "explanation": f"Verified as scientific fact in {scientific_result.get('fact_type', 'general')} domain. {scientific_result.get('reference', '')}",
                    "timestamp": datetime.now().isoformat(),
                    "evidence_count": len(scientific_result['sources']),
                    "all_claims": [primary_claim],
                    "method": "scientific_validation"
                }
            
            # Check against evidence database using pattern matching
            evidence_key = self._match_evidence_pattern(primary_claim)
            if evidence_key and evidence_key in self.evidence_db:
                evidence = self.evidence_db[evidence_key]
                return {
                    "claim": primary_claim,
                    "verdict": evidence['verdict'],
                    "confidence": evidence['confidence'],
                    "sources": evidence['sources'],
                    "explanation": evidence['explanation'],
                    "timestamp": datetime.now().isoformat(),
                    "evidence_count": len(evidence['sources']),
                    "all_claims": [primary_claim],
                    "method": "evidence_database"
                }
            
            # Default analysis for unknown claims
            return self._analyze_unknown_claim(primary_claim)
            
        except Exception as e:
            logger.error(f"Demo analysis error: {str(e)}")
            return {
                "claim": input_text,
                "verdict": "AMBIGUOUS",
                "confidence": 0,
                "sources": [],
                "explanation": f"Analysis failed due to technical error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": True
            }
    
    def _match_evidence_pattern(self, claim: str) -> str:
        """Match claim against known evidence patterns."""
        claim_lower = claim.lower()
        
        # Pattern matching for known claims
        patterns = {
            'vaccines_autism': ['vaccine', 'autism', 'cause'],
            'earth_round': ['earth', 'round', 'sphere'],
            'covid_vaccines_effective': ['covid', 'vaccine', 'effective'],
            '5g_coronavirus': ['5g', 'coronavirus', 'covid', 'cause'],
            'climate_change_hoax': ['climate change', 'hoax', 'fake'],
            'chocolate_happiness': ['chocolate', 'happy', 'mood']
        }
        
        for key, keywords in patterns.items():
            if all(keyword in claim_lower for keyword in keywords):
                return key
                
        return None
    
    def _analyze_unknown_claim(self, claim: str) -> Dict:
        """Analyze claims not in evidence database."""
        claim_lower = claim.lower()
        
        # Look for opinion indicators
        opinion_indicators = ['think', 'believe', 'feel', 'opinion', 'personally', 'best', 'worst']
        if any(indicator in claim_lower for indicator in opinion_indicators):
            return {
                "claim": claim,
                "verdict": "AMBIGUOUS",
                "confidence": 40,
                "sources": [],
                "explanation": "This appears to be an opinion or subjective statement rather than a factual claim.",
                "timestamp": datetime.now().isoformat(),
                "evidence_count": 0,
                "all_claims": [claim],
                "method": "opinion_detection"
            }
        
        # Look for conspiracy theory indicators
        conspiracy_keywords = ['secret', 'cover-up', 'conspiracy', 'they dont want you to know', 'hidden truth']
        if any(keyword in claim_lower for keyword in conspiracy_keywords):
            return {
                "claim": claim,
                "verdict": "FALSE",
                "confidence": 70,
                "sources": ['Pattern analysis'],
                "explanation": "This claim contains conspiracy theory language patterns that are typically associated with misinformation.",
                "timestamp": datetime.now().isoformat(),
                "evidence_count": 1,
                "all_claims": [claim],
                "method": "conspiracy_detection"
            }
        
        # Look for absolute statements without evidence
        absolute_keywords = ['always', 'never', 'all', 'none', 'every', 'completely']
        if any(keyword in claim_lower for keyword in absolute_keywords):
            return {
                "claim": claim,
                "verdict": "AMBIGUOUS",
                "confidence": 35,
                "sources": [],
                "explanation": "This claim makes absolute statements that are difficult to verify without specific evidence.",
                "timestamp": datetime.now().isoformat(),
                "evidence_count": 0,
                "all_claims": [claim],
                "method": "absolute_statement_detection"
            }
        
        # Default for unrecognized claims
        return {
            "claim": claim,
            "verdict": "AMBIGUOUS",
            "confidence": 30,
            "sources": [],
            "explanation": "Unable to find sufficient evidence to verify this claim. More research needed.",
            "timestamp": datetime.now().isoformat(),
            "evidence_count": 0,
            "all_claims": [claim],
            "method": "default_analysis"
        }