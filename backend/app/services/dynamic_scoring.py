"""Dynamic analysis methods for the industrial fact checker"""
from typing import Dict, List, Optional, Any
import re
import hashlib
import math

def calculate_dynamic_score(
    base_score: float,
    quality_impact: float,
    source_impact: float,
    kb_impact: float,
    content_hash_variation: float
) -> float:
    """Calculate final dynamic credibility score with multiple factors"""
    # Combine all impacts with their weights
    score = base_score
    
    # Quality impact (30% weight)
    score += quality_impact * 0.3
    
    # Source impact (20% weight)
    score += source_impact * 0.2
    
    # Knowledge base impact (25% weight)
    score += kb_impact * 0.25
    
    # Add small content-based variation
    score += content_hash_variation
    
    # Ensure score stays in valid range
    return max(5.0, min(95.0, score))

def analyze_credibility_signals(content: str) -> Dict[str, Any]:
    """Analyze various credibility signals in content"""
    signals = {
        'factual_language': len(re.findall(r'\b(study|research|evidence|data|analysis)\b', content.lower())),
        'qualified_claims': len(re.findall(r'\b(may|might|could|suggests?|indicates?)\b', content.lower())),
        'absolute_claims': len(re.findall(r'\b(always|never|everyone|no one|proves?|definitely)\b', content.lower())),
        'uncertainty_markers': len(re.findall(r'\b(possibly|perhaps|unclear|not certain|more research needed)\b', content.lower()))
    }
    
    score = min(100, sum([
        signals['factual_language'] * 5,
        signals['qualified_claims'] * 3,
        -signals['absolute_claims'] * 4,
        signals['uncertainty_markers'] * 2
    ]))
    
    return {'score': score, 'details': signals}

def calculate_factual_density(content: str) -> float:
    """Calculate the density of factual statements and data points"""
    total_words = len(content.split())
    if total_words == 0:
        return 0.0
        
    fact_patterns = [
        r'\b\d+(?:\.\d+)?%\b',  # Percentages
        r'\b(?:in|during|on)\s+\d{4}\b',  # Years
        r'\b\d+(?:\.\d+)?\s*(?:million|billion|trillion)\b',  # Large numbers
        r'\b(?:according to|cited by|reported by|study by)\b',  # Citations
        r'\b(?:increase(?:d|s)?|decrease(?:d|s)?|change(?:d|s)?)\s+by\s+\d+\b',  # Changes
        r'\b(?:approximately|estimated|averaged?|mean)\s+\d+\b'  # Statistical references
    ]
    
    fact_count = sum(len(re.findall(pattern, content.lower())) for pattern in fact_patterns)
    density = (fact_count * 100.0) / total_words
    
    return min(100.0, density * 10)

def generate_content_variation(content: str, range_size: float = 5.0) -> float:
    """Generate a deterministic but seemingly random variation based on content"""
    # Create a hash of the content
    content_hash = int(hashlib.md5(content.encode()).hexdigest(), 16)
    
    # Convert hash to a number in the desired range
    variation = ((content_hash % (int(range_size * 2 * 100))) / 100) - range_size
    
    return variation

def calculate_evidence_ratio(supporting: List[Dict], contradicting: List[Dict]) -> float:
    """Calculate the ratio of supporting to total evidence weight"""
    supporting_weight = sum(s.get('weight', 1.0) for s in supporting)
    contradicting_weight = sum(c.get('weight', 1.0) for c in contradicting)
    total_weight = supporting_weight + contradicting_weight
    
    if total_weight == 0:
        return 0.5  # Neutral when no evidence
        
    return supporting_weight / total_weight