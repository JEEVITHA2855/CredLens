import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re

class ClaimVerifier:
    def __init__(self):
        # Initialize with trusted fact-checking websites
        self.fact_check_sites = [
            "https://www.snopes.com/fact-check/",
            "https://www.factcheck.org/",
            "https://www.politifact.com/"
        ]
        
        # Initialize known facts database
        self.known_facts = {
            "astronomy": {
                "Earth revolves around Sun": True,
                "Earth is flat": False,
                "Moon orbits Earth": True
            },
            "science": {
                "Vaccines cause autism": False,
                "Evolution is scientifically proven": True,
                "Climate change is real": True
            },
            "health": {
                "Drinking water is healthy": True,
                "Smoking causes cancer": True,
                "Exercise improves health": True
            }
        }
        
    def verify_claim(self, claim):
        """Verify a claim using multiple methods."""
        try:
            result = {
                "is_factual": None,
                "confidence": 0,
                "reasoning": "",
                "supporting_facts": [],
                "contradicting_evidence": []
            }
            
            # 1. Check against known facts database
            for category, facts in self.known_facts.items():
                for fact, is_true in facts.items():
                    if self._text_similarity(claim.lower(), fact.lower()) > 0.7:
                        result["is_factual"] = is_true
                        result["confidence"] = 90
                        result["reasoning"] = f"Claim matches known {'fact' if is_true else 'misinformation'} in {category} category"
                        result["supporting_facts"].append(fact if is_true else f"This is a known false claim in {category}")
                        return result
            
            # 2. Check claim characteristics
            result = self._analyze_claim_characteristics(claim, result)
            
            return result
            
        except Exception as e:
            print(f"Error in claim analysis: {str(e)}")
            return {
                "is_factual": None,
                "confidence": 0,
                "reasoning": "Error in claim analysis",
                "supporting_facts": [],
                "contradicting_evidence": []
            }
    
    def _text_similarity(self, text1, text2):
        """Calculate similarity between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0
    
    def _analyze_claim_characteristics(self, claim, result):
        """Analyze characteristics of the claim."""
        # Check for scientific patterns
        if re.search(r'(study|research|scientists|evidence|data|proven)', claim, re.I):
            if not re.search(r'(shocking|secret|conspiracy|they don\'t want you to know)', claim, re.I):
                result["confidence"] += 20
                result["supporting_facts"].append("Claim references scientific concepts without sensational language")
        
        # Check for extreme language
        if re.search(r'(always|never|cure|miracle|secret|shocking|conspiracy)', claim, re.I):
            result["confidence"] -= 20
            result["contradicting_evidence"].append("Claim uses extreme or sensational language")
        
        # Check for measurable claims
        if re.search(r'(\d+%|\d+ times|increased|decreased)', claim, re.I):
            result["confidence"] += 10
            result["supporting_facts"].append("Claim makes specific, measurable assertions")
        
        # Make final determination
        result["is_factual"] = result["confidence"] >= 50
        result["reasoning"] = f"Based on language analysis and claim characteristics, confidence level: {result['confidence']}%"
        
        return result
