import re
from typing import Optional

def clean_text(text: str) -> str:
    """Clean and normalize text for processing"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove HTML entities
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    
    return text.strip()

def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return None

def is_suspicious_language(text: str, suspicious_words: list) -> tuple[bool, list]:
    """Check if text contains suspicious/sensational language"""
    text_lower = text.lower()
    found_words = []
    
    for word in suspicious_words:
        if word.lower() in text_lower:
            found_words.append(word)
    
    return len(found_words) > 0, found_words