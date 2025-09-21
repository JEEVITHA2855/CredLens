import re
from typing import List, Tuple
from ..models.claim import CredibilityFingerprint, SuspiciousPhrase, Evidence
from ..config import SUSPICIOUS_WORDS, CREDIBILITY_THRESHOLDS
from ..utils.text_processing import is_suspicious_language
from ..utils.url_handler import URLHandler

class CredibilityScorer:
    def __init__(self):
        self.url_handler = URLHandler()
        
    def calculate_credibility_fingerprint(
        self, 
        claim: str, 
        evidence_list: List[Evidence],
        source_url: str = None
    ) -> CredibilityFingerprint:
        """Calculate comprehensive credibility fingerprint"""
        
        # 1. Source Credibility (if URL provided)
        source_credibility = self._calculate_source_credibility(source_url, evidence_list)
        
        # 2. Corroboration Count
        corroboration_count = self._calculate_corroboration_count(evidence_list)
        
        # 3. Language Risk Score
        language_risk = self._calculate_language_risk(claim)
        
        # 4. Overall Score (weighted combination)
        overall_score = self._calculate_overall_score(
            source_credibility, corroboration_count, language_risk, evidence_list
        )
        
        return CredibilityFingerprint(
            source_credibility=source_credibility,
            corroboration_count=corroboration_count,
            language_risk=language_risk,
            overall_score=overall_score
        )
    
    def find_suspicious_phrases(self, text: str) -> List[SuspiciousPhrase]:
        """Find suspicious/sensational phrases in text"""
        suspicious_phrases = []
        text_lower = text.lower()
        
        # Check for suspicious words
        is_suspicious, found_words = is_suspicious_language(text, SUSPICIOUS_WORDS)
        
        if is_suspicious:
            for word in found_words:
                # Find all occurrences of the word
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                for match in pattern.finditer(text):
                    phrase = SuspiciousPhrase(
                        phrase=match.group(),
                        start_pos=match.start(),
                        end_pos=match.end(),
                        reason="Sensational/emotional language"
                    )
                    suspicious_phrases.append(phrase)
        
        # Check for excessive punctuation
        exclamation_pattern = r'!{2,}'
        for match in re.finditer(exclamation_pattern, text):
            phrase = SuspiciousPhrase(
                phrase=match.group(),
                start_pos=match.start(),
                end_pos=match.end(),
                reason="Excessive punctuation (emotional appeal)"
            )
            suspicious_phrases.append(phrase)
        
        # Check for ALL CAPS words
        caps_pattern = r'\b[A-Z]{3,}\b'
        for match in re.finditer(caps_pattern, text):
            if match.group() not in ['USA', 'FBI', 'CIA', 'WHO', 'NASA', 'CEO']:  # Exclude common acronyms
                phrase = SuspiciousPhrase(
                    phrase=match.group(),
                    start_pos=match.start(),
                    end_pos=match.end(),
                    reason="Excessive capitalization (emphasis/shouting)"
                )
                suspicious_phrases.append(phrase)
        
        return suspicious_phrases
    
    def _calculate_source_credibility(self, source_url: str, evidence_list: List[Evidence]) -> float:
        """Calculate source credibility score"""
        if source_url:
            try:
                from urllib.parse import urlparse
                domain = urlparse(source_url).netloc
                return self.url_handler.get_source_credibility(domain)
            except:
                pass
        
        # If no source URL, use average of evidence sources
        if evidence_list:
            credibility_scores = []
            for evidence in evidence_list:
                if evidence.url:
                    try:
                        from urllib.parse import urlparse
                        domain = urlparse(evidence.url).netloc
                        score = self.url_handler.get_source_credibility(domain)
                        credibility_scores.append(score)
                    except:
                        pass
            
            if credibility_scores:
                return sum(credibility_scores) / len(credibility_scores)
        
        return 0.5  # Default/unknown
    
    def _calculate_corroboration_count(self, evidence_list: List[Evidence]) -> int:
        """Calculate number of corroborating sources"""
        # Count evidence that supports the claim
        supporting_evidence = [
            e for e in evidence_list 
            if e.nli_label == "ENTAILMENT" and e.confidence > 0.5
        ]
        return len(supporting_evidence)
    
    def _calculate_language_risk(self, text: str) -> float:
        """Calculate language risk score (higher = more risky)"""
        risk_score = 0.0
        
        # Check for suspicious words
        is_suspicious, found_words = is_suspicious_language(text, SUSPICIOUS_WORDS)
        if is_suspicious:
            risk_score += min(0.5, len(found_words) * 0.1)
        
        # Check for excessive punctuation
        exclamation_count = text.count('!')
        if exclamation_count > 2:
            risk_score += min(0.2, exclamation_count * 0.05)
        
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.1:
            risk_score += min(0.3, caps_ratio)
        
        return min(1.0, risk_score)
    
    def _calculate_overall_score(
        self, 
        source_credibility: float, 
        corroboration_count: int, 
        language_risk: float,
        evidence_list: List[Evidence]
    ) -> float:
        """Calculate overall credibility score"""
        
        # Base score from source credibility (40% weight)
        score = source_credibility * 0.4
        
        # Add corroboration bonus (30% weight)
        corroboration_bonus = min(0.3, corroboration_count * 0.1)
        score += corroboration_bonus
        
        # Subtract language risk penalty (20% weight)
        language_penalty = language_risk * 0.2
        score -= language_penalty
        
        # Evidence quality bonus (10% weight)
        if evidence_list:
            avg_confidence = sum(e.confidence for e in evidence_list) / len(evidence_list)
            evidence_bonus = avg_confidence * 0.1
            score += evidence_bonus
        
        return max(0.0, min(1.0, score))
    
    def get_credibility_level(self, score: float) -> str:
        """Convert credibility score to level"""
        if score >= CREDIBILITY_THRESHOLDS["high"]:
            return "High"
        elif score >= CREDIBILITY_THRESHOLDS["medium"]:
            return "Medium"
        else:
            return "Low"