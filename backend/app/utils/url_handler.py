import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Optional

class URLHandler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract_content(self, url: str) -> tuple[str, str, str]:
        """Extract title, content, and domain from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Extract title
            title_elem = soup.find('title')
            title = title_elem.get_text().strip() if title_elem else ""
            
            # Extract main content using various selectors
            content_selectors = [
                'article',
                'main',
                '[role="main"]',
                '.content',
                '.post-content',
                '.article-content',
                '.story-content',
                '.entry-content',
                '.post-body',
                '.article-body',
                '.story-body'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = ' '.join([elem.get_text().strip() for elem in elements])
                    break
            
            # Fallback to paragraphs if no main content found
            if not content:
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs[:10]])
            
            # Get domain
            domain = urlparse(url).netloc
            
            return title, content, domain
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to parse content: {str(e)}")
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and accessible"""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and parsed.scheme in ('http', 'https')
        except:
            return False
    
    def get_source_credibility(self, domain: str) -> float:
        """Get basic credibility score for a domain"""
        # This is a simplified credibility scoring
        # In a real system, this would use a comprehensive database
        trusted_sources = {
            'reuters.com': 0.95,
            'apnews.com': 0.95,
            'bbc.com': 0.90,
            'cnn.com': 0.85,
            'nytimes.com': 0.90,
            'washingtonpost.com': 0.88,
            'npr.org': 0.90,
            'pbs.org': 0.88,
            'factcheck.org': 0.95,
            'snopes.com': 0.92,
            'politifact.com': 0.90,
            'wikipedia.org': 0.75,
        }
        
        questionable_sources = {
            'infowars.com': 0.15,
            'naturalnews.com': 0.20,
            'beforeitsnews.com': 0.25,
        }
        
        domain_lower = domain.lower()
        
        # Check trusted sources
        for trusted_domain, score in trusted_sources.items():
            if trusted_domain in domain_lower:
                return score
        
        # Check questionable sources
        for questionable_domain, score in questionable_sources.items():
            if questionable_domain in domain_lower:
                return score
        
        # Default score for unknown sources
        return 0.5