"""
Advanced AI-powered misinformation detection system with dynamic evidence retrieval.
"""
import os
import json
import requests
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import re
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

class EvidenceRetriever:
    """Retrieves evidence from multiple trusted sources."""
    
    def __init__(self):
        self.bing_api_key = os.getenv('BING_SEARCH_API_KEY')
        self.google_cse_id = os.getenv('GOOGLE_CSE_ID')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.wikipedia_base_url = "https://en.wikipedia.org/api/rest_v1/page/summary"
        self.bing_search_url = "https://api.bing.microsoft.com/v7.0/search"
        
        # Trusted source domains
        self.trusted_domains = [
            'who.int', 'cdc.gov', 'nature.com', 'science.org', 'nejm.org',
            'bbc.com', 'reuters.com', 'ap.org', 'theguardian.com',
            'nytimes.com', 'washingtonpost.com', 'nasa.gov', 'nih.gov',
            'mayoclinic.org', 'webmd.com', 'britannica.com'
        ]
    
    def search_wikipedia(self, query: str) -> Dict:
        """Search Wikipedia for factual information."""
        try:
            # Clean query for Wikipedia search
            clean_query = re.sub(r'[^\w\s]', '', query).replace(' ', '_')
            response = requests.get(f"{self.wikipedia_base_url}/{clean_query}")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'found': True,
                    'title': data.get('title', ''),
                    'extract': data.get('extract', ''),
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'source': 'Wikipedia'
                }
            else:
                # Try alternative search if direct page not found
                search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={quote_plus(query)}&limit=1&format=json"
                search_response = requests.get(search_url)
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    if len(search_data[1]) > 0:
                        page_title = search_data[1][0].replace(' ', '_')
                        page_response = requests.get(f"{self.wikipedia_base_url}/{page_title}")
                        if page_response.status_code == 200:
                            page_data = page_response.json()
                            return {
                                'found': True,
                                'title': page_data.get('title', ''),
                                'extract': page_data.get('extract', ''),
                                'url': page_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                                'source': 'Wikipedia'
                            }
                        
        except Exception as e:
            logger.error(f"Wikipedia search error: {str(e)}")
            
        return {'found': False, 'error': 'No Wikipedia results found'}
    
    def search_bing(self, query: str) -> List[Dict]:
        """Search Bing for recent news and authoritative sources."""
        if not self.bing_api_key:
            return []
            
        try:
            headers = {'Ocp-Apim-Subscription-Key': self.bing_api_key}
            params = {
                'q': query,
                'count': 10,
                'mkt': 'en-US',
                'safeSearch': 'Strict'
            }
            
            response = requests.get(self.bing_search_url, headers=headers, params=params)
            response.raise_for_status()
            
            results = []
            data = response.json()
            
            for item in data.get('webPages', {}).get('value', []):
                url = item.get('url', '')
                domain = self._extract_domain(url)
                
                # Prioritize trusted sources
                if any(trusted in domain for trusted in self.trusted_domains):
                    results.append({
                        'title': item.get('name', ''),
                        'snippet': item.get('snippet', ''),
                        'url': url,
                        'domain': domain,
                        'source': 'Bing Search (Trusted)',
                        'trusted': True
                    })
                elif len(results) < 5:  # Include some non-trusted but relevant sources
                    results.append({
                        'title': item.get('name', ''),
                        'snippet': item.get('snippet', ''),
                        'url': url,
                        'domain': domain,
                        'source': 'Bing Search',
                        'trusted': False
                    })
                    
            return results[:5]  # Return top 5 results
            
        except Exception as e:
            logger.error(f"Bing search error: {str(e)}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.lower()
        except:
            return ''

class ClaimExtractor:
    """Extracts core factual claims from input text."""
    
    def extract_claims(self, text: str) -> List[str]:
        """Extract main factual claims from text."""
        # Remove common opinion indicators
        opinion_indicators = [
            'i think', 'i believe', 'in my opinion', 'personally',
            'i feel', 'it seems', 'probably', 'maybe', 'perhaps'
        ]
        
        cleaned_text = text.lower()
        for indicator in opinion_indicators:
            cleaned_text = cleaned_text.replace(indicator, '')
        
        # Split into sentences and filter factual claims
        sentences = re.split(r'[.!?]+', text.strip())
        claims = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Filter out very short fragments
                # Look for factual statements (contains specific facts, numbers, etc.)
                if self._is_factual_claim(sentence):
                    claims.append(sentence)
                    
        return claims if claims else [text.strip()]  # Return original if no specific claims found
    
    def _is_factual_claim(self, sentence: str) -> bool:
        """Determine if a sentence contains factual claims."""
        factual_indicators = [
            r'\d+',  # Contains numbers
            r'(cause|causes|caused)',  # Causal statements
            r'(is|are|was|were|will be|has|have)',  # Definitive statements
            r'(always|never|all|every|no|none)',  # Absolute statements
            r'(proven|proved|study|research|scientist)',  # Scientific claims
        ]
        
        for pattern in factual_indicators:
            if re.search(pattern, sentence.lower()):
                return True
        return False

class AIVerifier:
    """AI-powered claim verification using retrieved evidence."""
    
    def __init__(self):
        self.evidence_weight = {
            'Wikipedia': 0.8,
            'Bing Search (Trusted)': 0.9,
            'Bing Search': 0.6,
            'Scientific': 0.95
        }
    
    def verify_claim(self, claim: str, evidence: List[Dict]) -> Dict:
        """Verify claim against retrieved evidence."""
        if not evidence:
            return {
                'verdict': 'AMBIGUOUS',
                'confidence': 25,
                'explanation': 'No reliable evidence found to verify this claim.',
                'sources': []
            }
        
        # Analyze evidence
        support_score = 0
        refute_score = 0
        total_weight = 0
        supporting_sources = []
        refuting_sources = []
        
        for item in evidence:
            weight = self.evidence_weight.get(item.get('source', 'Unknown'), 0.5)
            total_weight += weight
            
            # Simple keyword-based analysis (can be enhanced with ML)
            content = (item.get('extract', '') + ' ' + item.get('snippet', '')).lower()
            claim_lower = claim.lower()
            
            # Extract key terms from claim
            key_terms = self._extract_key_terms(claim_lower)
            
            # Check for supporting/refuting language
            support_keywords = ['true', 'correct', 'accurate', 'confirmed', 'proven', 'verified']
            refute_keywords = ['false', 'incorrect', 'debunked', 'myth', 'no evidence', 'no link']
            
            term_matches = sum(1 for term in key_terms if term in content)
            support_matches = sum(1 for keyword in support_keywords if keyword in content)
            refute_matches = sum(1 for keyword in refute_keywords if keyword in content)
            
            if refute_matches > support_matches and term_matches > 0:
                refute_score += weight
                refuting_sources.append(item.get('url', ''))
            elif support_matches > 0 and term_matches > 0:
                support_score += weight
                supporting_sources.append(item.get('url', ''))
            elif term_matches > len(key_terms) // 2:  # Neutral mention
                support_score += weight * 0.3
                supporting_sources.append(item.get('url', ''))
        
        # Determine verdict
        if total_weight == 0:
            return {
                'verdict': 'AMBIGUOUS',
                'confidence': 20,
                'explanation': 'Insufficient evidence to make a determination.'
            }
        
        support_ratio = support_score / total_weight
        refute_ratio = refute_score / total_weight
        
        if refute_ratio > 0.6:
            verdict = 'FALSE'
            confidence = min(95, int(refute_ratio * 100))
            explanation = f"Multiple reliable sources contradict this claim. Evidence strongly suggests this is false."
            sources = refuting_sources
        elif support_ratio > 0.6:
            verdict = 'TRUE'
            confidence = min(95, int(support_ratio * 100))
            explanation = f"Multiple reliable sources support this claim. Evidence suggests this is accurate."
            sources = supporting_sources
        elif abs(support_ratio - refute_ratio) < 0.2:
            verdict = 'AMBIGUOUS'
            confidence = 40
            explanation = f"Sources present conflicting information. More research needed for definitive answer."
            sources = supporting_sources + refuting_sources
        else:
            # Lean towards the higher score but with lower confidence
            if support_ratio > refute_ratio:
                verdict = 'TRUE'
                confidence = min(75, int(support_ratio * 80))
                explanation = f"Some evidence supports this claim, but verification is not definitive."
                sources = supporting_sources
            else:
                verdict = 'FALSE'
                confidence = min(75, int(refute_ratio * 80))
                explanation = f"Some evidence contradicts this claim, but verification is not definitive."
                sources = refuting_sources
        
        return {
            'verdict': verdict,
            'confidence': confidence,
            'explanation': explanation,
            'sources': sources[:3] if sources else []  # Ensure sources is always a list
        }
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from claim text."""
        # Remove common words and extract meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if len(word) > 2 and word not in stop_words]

class AdvancedMisinformationDetector:
    """Main class that orchestrates the misinformation detection pipeline."""
    
    def __init__(self):
        self.claim_extractor = ClaimExtractor()
        self.evidence_retriever = EvidenceRetriever()
        self.ai_verifier = AIVerifier()
    
    def analyze(self, input_text: str) -> Dict:
        """Main analysis pipeline."""
        try:
            # Step 1: Extract core claims
            claims = self.claim_extractor.extract_claims(input_text)
            primary_claim = claims[0] if claims else input_text
            
            logger.info(f"Extracted claim: {primary_claim}")
            
            # Step 2: Retrieve evidence
            evidence = []
            
            # Wikipedia search
            wiki_result = self.evidence_retriever.search_wikipedia(primary_claim)
            if wiki_result.get('found'):
                evidence.append(wiki_result)
            
            # Bing search
            bing_results = self.evidence_retriever.search_bing(primary_claim)
            evidence.extend(bing_results)
            
            logger.info(f"Retrieved {len(evidence)} pieces of evidence")
            
            # Step 3: AI verification
            verification = self.ai_verifier.verify_claim(primary_claim, evidence)
            
            # Step 4: Format output
            result = {
                "claim": primary_claim,
                "verdict": verification['verdict'],
                "confidence": verification['confidence'],
                "sources": verification['sources'],
                "explanation": verification['explanation'],
                "timestamp": datetime.now().isoformat(),
                "evidence_count": len(evidence),
                "all_claims": claims
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return {
                "claim": input_text,
                "verdict": "AMBIGUOUS",
                "confidence": 0,
                "sources": [],
                "explanation": f"Analysis failed due to technical error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": True
            }