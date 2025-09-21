"""
Evidence-based claim verification service
Analyzes claims against provided evidence from reliable sources
"""
from typing import List, Dict, Tuple
import re
from datetime import datetime

class EvidenceBasedVerifier:
    def __init__(self):
        # Source reliability rankings
        self.source_rankings = {
            # Tier 1: Highest reliability (90-100%)
            'nature.com': 95, 'science.org': 95, 'nejm.org': 95, 'thelancet.com': 95,
            'who.int': 95, 'cdc.gov': 95, 'nih.gov': 95, 'nasa.gov': 95, 'noaa.gov': 95,
            'reuters.com': 90, 'ap.org': 90, 'bbc.com': 90, 'npr.org': 90,
            'factcheck.org': 90, 'snopes.com': 90, 'politifact.com': 90,
            
            # Tier 2: High reliability (75-89%)
            'nytimes.com': 85, 'washingtonpost.com': 85, 'theguardian.com': 85,
            'wsj.com': 85, 'economist.com': 85, 'wikipedia.org': 80,
            'pubmed.ncbi.nlm.nih.gov': 85, 'cochrane.org': 85,
            
            # Tier 3: Medium reliability (60-74%)
            'cnn.com': 70, 'nbcnews.com': 70, 'cbsnews.com': 70, 'abcnews.go.com': 70,
            'usatoday.com': 65, 'time.com': 65, 'newsweek.com': 65,
            
            # Default for unknown sources
            'unknown': 50
        }
        
        # Sensational/manipulative language patterns
        self.sensational_patterns = [
            r'\bSHOCKING\b', r'\bUNBELIEVABLE\b', r'\bSTUNNING\b', r'\bEXPLOSIVE\b',
            r'\bSECRET\b', r'\bHIDDEN\b', r'\bCOVER-UP\b', r'\bCONSPIRACY\b',
            r'\bTHEY DON\'T WANT YOU TO KNOW\b', r'\bMAINSTREAM MEDIA\b',
            r'!!+', r'\bCLICK HERE\b', r'\bYOU WON\'T BELIEVE\b',
            r'\bDOCTORS HATE\b', r'\bTHIS ONE TRICK\b'
        ]
    
    def verify_with_evidence(self, claim: str, evidence_sources: List[Dict]) -> Dict:
        """
        Verify a claim against provided evidence sources
        
        Args:
            claim: The claim to verify
            evidence_sources: List of dicts with keys: 'source', 'content', 'url'
        
        Returns:
            Analysis result with verdict, reasoning, and scores
        """
        
        # Analyze the evidence
        supporting_evidence = []
        contradicting_evidence = []
        neutral_evidence = []
        
        source_trust_scores = []
        
        for evidence in evidence_sources:
            analysis = self._analyze_evidence_piece(claim, evidence)
            
            if analysis['stance'] == 'supporting':
                supporting_evidence.append(analysis)
            elif analysis['stance'] == 'contradicting':
                contradicting_evidence.append(analysis)
            else:
                neutral_evidence.append(analysis)
            
            source_trust_scores.append(analysis['source_trust'])
        
        # Determine verdict
        verdict = self._determine_verdict(supporting_evidence, contradicting_evidence, neutral_evidence)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(claim, supporting_evidence, contradicting_evidence, verdict)
        
        # Calculate scores
        scores = self._calculate_scores(
            claim, supporting_evidence, contradicting_evidence, 
            neutral_evidence, source_trust_scores, verdict
        )
        
        return {
            'claim': claim,
            'verdict': verdict,
            'reasoning': reasoning,
            'scores': scores,
            'evidence_breakdown': {
                'supporting': len(supporting_evidence),
                'contradicting': len(contradicting_evidence),
                'neutral': len(neutral_evidence),
                'total_sources': len(evidence_sources)
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_evidence_piece(self, claim: str, evidence: Dict) -> Dict:
        """Analyze a single piece of evidence"""
        content = evidence.get('content', '').lower()
        source_url = evidence.get('url', evidence.get('source', ''))
        
        # Extract domain for trust scoring
        domain = self._extract_domain(source_url)
        source_trust = self.source_rankings.get(domain, self.source_rankings['unknown'])
        
        # Improved keyword matching for stance
        claim_lower = claim.lower()
        
        supporting_indicators = 0
        contradicting_indicators = 0
        
        # Check for direct support
        if any(phrase in content for phrase in ['safe and effective', 'proven safe', 'demonstrated safety', 'rigorous clinical trials']):
            supporting_indicators += 2
        elif any(phrase in content for phrase in ['confirmed', 'verified', 'evidence shows', 'research indicates']):
            supporting_indicators += 1
            
        # Check for contradiction
        if any(phrase in content for phrase in ['not safe', 'dangerous', 'harmful', 'unsafe']):
            contradicting_indicators += 2
        elif any(phrase in content for phrase in ['false', 'debunked', 'incorrect', 'no evidence', 'myth']):
            contradicting_indicators += 1
        
        # Check for specific claim keywords in content
        if 'vaccine' in claim_lower and 'vaccine' in content:
            if any(word in content for word in ['safe', 'effective', 'efficacy']):
                supporting_indicators += 1
        
        # Determine stance
        if supporting_indicators > contradicting_indicators and supporting_indicators > 0:
            stance = 'supporting'
        elif contradicting_indicators > supporting_indicators and contradicting_indicators > 0:
            stance = 'contradicting'
        else:
            stance = 'neutral'
        
        return {
            'content': evidence.get('content', ''),
            'source': source_url,
            'domain': domain,
            'source_trust': source_trust,
            'stance': stance,
            'relevance_score': min(supporting_indicators + contradicting_indicators, 10) / 10
        }
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        import re
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        return match.group(1) if match else 'unknown'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract key terms from text"""
        # Remove common words and extract meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return [word for word in words if word not in stop_words][:8]
    
    def _determine_verdict(self, supporting: List, contradicting: List, neutral: List) -> str:
        """Determine the final verdict based on evidence"""
        
        # Weight by source trust
        supporting_weight = sum(e['source_trust'] * e['relevance_score'] for e in supporting)
        contradicting_weight = sum(e['source_trust'] * e['relevance_score'] for e in contradicting)
        
        total_evidence = len(supporting) + len(contradicting) + len(neutral)
        
        # Need substantial evidence for definitive verdict
        if total_evidence < 2:
            return 'AMBIGUOUS'
        
        # Strong support threshold
        if supporting_weight > contradicting_weight * 2 and len(supporting) >= 2:
            return 'TRUE'
        
        # Strong contradiction threshold  
        if contradicting_weight > supporting_weight * 2 and len(contradicting) >= 2:
            return 'FALSE'
        
        # Mixed or insufficient evidence
        return 'AMBIGUOUS'
    
    def _generate_reasoning(self, claim: str, supporting: List, contradicting: List, verdict: str) -> str:
        """Generate explanation for the verdict"""
        
        total_sources = len(supporting) + len(contradicting)
        
        if verdict == 'TRUE':
            high_trust_supporting = [e for e in supporting if e['source_trust'] >= 85]
            reasoning = f"The claim is supported by {len(supporting)} sources, "
            if high_trust_supporting:
                reasoning += f"including {len(high_trust_supporting)} highly reliable sources. "
            reasoning += "Evidence consistently confirms the claim's accuracy."
            
        elif verdict == 'FALSE':
            high_trust_contradicting = [e for e in contradicting if e['source_trust'] >= 85]
            reasoning = f"The claim is contradicted by {len(contradicting)} sources, "
            if high_trust_contradicting:
                reasoning += f"including {len(high_trust_contradicting)} highly reliable sources. "
            reasoning += "Evidence shows the claim is factually incorrect."
            
        else:  # AMBIGUOUS
            reasoning = f"Evidence is mixed or insufficient with {len(supporting)} supporting and {len(contradicting)} contradicting sources. "
            if total_sources < 3:
                reasoning += "More evidence needed for definitive assessment."
            else:
                reasoning += "Claims requires additional context or has conflicting interpretations."
        
        return reasoning
    
    def _calculate_scores(self, claim: str, supporting: List, contradicting: List, 
                         neutral: List, source_trust_scores: List, verdict: str) -> Dict:
        """Calculate credibility scores"""
        
        # Overall Credibility based on verdict and evidence strength
        if verdict == 'TRUE':
            overall_credibility = min(95, 60 + len(supporting) * 10)
        elif verdict == 'FALSE':
            overall_credibility = max(5, 40 - len(contradicting) * 10)
        else:
            overall_credibility = 50
        
        # Source Trust - average of all source trust scores
        avg_source_trust = sum(source_trust_scores) / len(source_trust_scores) if source_trust_scores else 50
        
        # Corroboration - number of sources that support the verdict
        if verdict == 'TRUE':
            corroboration = len(supporting)
        elif verdict == 'FALSE':
            corroboration = len(contradicting)
        else:
            corroboration = max(len(supporting), len(contradicting))
        
        # Language Safety - check for sensational language in claim
        language_safety = 100
        for pattern in self.sensational_patterns:
            if re.search(pattern, claim, re.IGNORECASE):
                language_safety -= 15
        language_safety = max(0, language_safety)
        
        return {
            'overall_credibility': int(overall_credibility),
            'source_trust': int(avg_source_trust),
            'corroboration': corroboration,
            'language_safety': int(language_safety)
        }

# Example usage and testing
if __name__ == "__main__":
    verifier = EvidenceBasedVerifier()
    
    # Test with sample evidence
    claim = "COVID-19 vaccines are safe and effective"
    
    evidence_sources = [
        {
            'source': 'https://www.cdc.gov/coronavirus/2019-ncov/vaccines/safety/safety-of-vaccines.html',
            'content': 'COVID-19 vaccines are safe and effective. They underwent rigorous clinical trials and continue to be monitored.',
            'url': 'https://www.cdc.gov/coronavirus/2019-ncov/vaccines/safety/'
        },
        {
            'source': 'https://www.who.int/news-room/q-a-detail/coronavirus-disease-(covid-19)-vaccines',
            'content': 'WHO confirms COVID-19 vaccines have been proven safe and effective in preventing severe disease.',
            'url': 'https://www.who.int/news-room/q-a-detail/coronavirus-disease-(covid-19)-vaccines'
        },
        {
            'source': 'https://www.nejm.org/doi/full/10.1056/NEJMoa2034577',
            'content': 'Clinical trial results demonstrate 95% efficacy and good safety profile for COVID-19 vaccine.',
            'url': 'https://www.nejm.org/doi/full/10.1056/NEJMoa2034577'
        }
    ]
    
    result = verifier.verify_with_evidence(claim, evidence_sources)
    
    print("Evidence-Based Fact Check Result:")
    print("=" * 50)
    print(f"Claim: {result['claim']}")
    print(f"Verdict: {result['verdict']}")
    print(f"Reason: {result['reasoning']}")
    print("Scores:")
    print(f"- Overall Credibility: {result['scores']['overall_credibility']}%")
    print(f"- Source Trust: {result['scores']['source_trust']}%")
    print(f"- Corroboration: {result['scores']['corroboration']} sources")
    print(f"- Language Safety: {result['scores']['language_safety']}%")