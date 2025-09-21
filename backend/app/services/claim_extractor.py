import re
import nltk
from nltk.tokenize import sent_tokenize
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from ..utils.text_processing import clean_text

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class ClaimExtractor:
    def __init__(self):
        self.claim_patterns = [
            r"According to.*?,\s*(.+?)(?:\.|$)",
            r"Studies show that\s*(.+?)(?:\.|$)",
            r"Research indicates\s*(.+?)(?:\.|$)",
            r"It is reported that\s*(.+?)(?:\.|$)",
            r"Scientists claim\s*(.+?)(?:\.|$)",
            r"Experts say\s*(.+?)(?:\.|$)",
            r"(.+?)\s*is\s*(?:true|false|correct|incorrect|proven|disproven)",
            r"The fact is\s*(.+?)(?:\.|$)",
            r"It has been proven that\s*(.+?)(?:\.|$)",
        ]
    
    def extract_from_text(self, text: str) -> str:
        """Extract the main factual claim from text"""
        if not text:
            return ""
        
        # Clean the text
        text = clean_text(text)
        
        # Try pattern-based extraction first
        claim = self._extract_with_patterns(text)
        if claim:
            return claim
        
        # Fall back to sentence-based extraction
        return self._extract_main_sentence(text)
    
    def extract_from_url(self, url: str) -> tuple[str, str]:
        """Extract claim from URL content"""
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get title and main content
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Extract main content
            content_selectors = [
                'article', 'main', '.content', '.post-content',
                '.article-body', '.story-body', 'p'
            ]
            
            content_text = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content_text = ' '.join([elem.get_text().strip() for elem in elements[:5]])
                    break
            
            if not content_text:
                content_text = soup.get_text()
            
            # Combine title and content for claim extraction
            full_text = f"{title_text}. {content_text}"
            claim = self.extract_from_text(full_text)
            
            return claim, full_text
            
        except Exception as e:
            raise Exception(f"Failed to extract content from URL: {str(e)}")
    
    def _extract_with_patterns(self, text: str) -> Optional[str]:
        """Try to extract claim using predefined patterns"""
        for pattern in self.claim_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                claim = matches[0].strip()
                if len(claim) > 20 and len(claim) < 500:  # Reasonable claim length
                    return claim
        return None
    
    def _extract_main_sentence(self, text: str) -> str:
        """Extract the most likely claim sentence"""
        sentences = sent_tokenize(text)
        
        if not sentences:
            return text[:200] if len(text) > 200 else text
        
        # Score sentences based on claim indicators
        scored_sentences = []
        for sentence in sentences:
            score = self._score_sentence_as_claim(sentence)
            if score > 0:
                scored_sentences.append((sentence, score))
        
        if scored_sentences:
            # Return the highest scoring sentence
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            return scored_sentences[0][0]
        
        # Fallback: return first substantial sentence
        for sentence in sentences:
            if len(sentence.split()) > 5:
                return sentence
        
        return sentences[0] if sentences else text[:200]
    
    def _score_sentence_as_claim(self, sentence: str) -> float:
        """Score how likely a sentence is to be a factual claim"""
        score = 0.0
        sentence_lower = sentence.lower()
        
        # Positive indicators
        claim_indicators = [
            'is', 'are', 'was', 'were', 'will', 'would', 'can', 'could',
            'shows', 'proves', 'indicates', 'reveals', 'confirms',
            'according to', 'study', 'research', 'report', 'data'
        ]
        
        for indicator in claim_indicators:
            if indicator in sentence_lower:
                score += 0.1
        
        # Negative indicators (questions, instructions, etc.)
        negative_indicators = ['?', 'how to', 'what is', 'click here', 'subscribe']
        for indicator in negative_indicators:
            if indicator in sentence_lower:
                score -= 0.2
        
        # Length bonus (claims are usually substantial)
        word_count = len(sentence.split())
        if 10 <= word_count <= 50:
            score += 0.2
        
        return max(0, score)