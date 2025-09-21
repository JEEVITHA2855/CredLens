"""
Google Gemini Fact-Checker for CredLens
=======================================

Advanced fact-checking using Google's Gemini AI with real-time search capabilities.
Much more cost-effective than OpenAI and includes access to current information.

Features:
- Free tier: 1,500 requests/day
- Real-time information access
- Multimodal capabilities
- Large context window (1M tokens)
- Better fact-checking accuracy
"""

import os
import json
import logging
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  Google Generative AI not installed. Run: pip install google-generativeai")

logger = logging.getLogger(__name__)

class GeminiFactChecker:
    """Advanced fact-checking using Google Gemini with real-time search."""
    
    def __init__(self):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai package not installed")
            
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 1.5 Flash (free tier: 15 RPM, 1,500 RPD)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Gemini Pro for complex analysis (if needed)
        self.pro_model = genai.GenerativeModel('gemini-1.5-pro')
        
        logger.info("Gemini Fact Checker initialized")
    
    def fact_check_claim(self, claim: str, use_pro_model: bool = False) -> Dict:
        """
        Fact-check a claim using Google Gemini with real-time information access.
        
        Args:
            claim (str): The claim to fact-check
            use_pro_model (bool): Use Gemini Pro for complex analysis
            
        Returns:
            dict: Comprehensive fact-check result
        """
        try:
            model = self.pro_model if use_pro_model else self.model
            prompt = self._create_fact_check_prompt(claim)
            
            # Generate response
            response = model.generate_content(prompt)
            
            # Parse response
            result = self._parse_gemini_response(response.text, claim)
            result['model_used'] = 'gemini-1.5-pro' if use_pro_model else 'gemini-1.5-flash'
            result['timestamp'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            logger.error(f"Gemini fact-check error: {str(e)}")
            return self._create_error_response(claim, str(e))
    
    def _create_fact_check_prompt(self, claim: str) -> str:
        """Create optimized prompt for Gemini fact-checking."""
        return f"""You are an expert fact-checker with access to real-time information. 
Analyze this claim and provide a comprehensive fact-check:

CLAIM: "{claim}"

Please provide your analysis in this exact JSON format:
{{
    "verdict": "TRUE" | "FALSE" | "AMBIGUOUS",
    "confidence": <number 0-100>,
    "explanation": "<detailed explanation of your reasoning>",
    "evidence_for": ["<supporting evidence point 1>", "<point 2>", "..."],
    "evidence_against": ["<contradicting evidence point 1>", "<point 2>", "..."],
    "sources": ["<authoritative source 1>", "<source 2>", "..."],
    "context": "<relevant background context>",
    "warnings": ["<any warnings about the claim>"],
    "related_facts": ["<related factual information>"],
    "last_updated": "<when this information was last verified>",
    "search_terms_used": ["<terms you searched for verification>"]
}}

IMPORTANT INSTRUCTIONS:
1. Use your real-time search capabilities to verify current information
2. Cite specific, authoritative sources (government, academic, established news)
3. Be especially careful with medical, scientific, and political claims
4. If the claim could cause harm if false, mark it clearly
5. Provide confidence based on quality and quantity of evidence
6. Include context that helps users understand the full picture
7. Search for both supporting and contradicting evidence
8. Check multiple independent sources before concluding

Analyze thoroughly and respond ONLY with the JSON format above."""
    
    def _parse_gemini_response(self, response_text: str, claim: str) -> Dict:
        """Parse Gemini's response into structured format."""
        try:
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_text = response_text[json_start:json_end]
            result = json.loads(json_text)
            
            # Ensure required fields
            result['claim'] = claim
            result['method'] = 'gemini_ai_with_search'
            
            # Validate and clean data
            result['confidence'] = min(max(int(result.get('confidence', 50)), 0), 100)
            result['verdict'] = result.get('verdict', 'AMBIGUOUS').upper()
            
            if result['verdict'] not in ['TRUE', 'FALSE', 'AMBIGUOUS']:
                result['verdict'] = 'AMBIGUOUS'
            
            # Ensure lists exist
            for field in ['evidence_for', 'evidence_against', 'sources', 'warnings', 'related_facts', 'search_terms_used']:
                if field not in result or not isinstance(result[field], list):
                    result[field] = []
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to parse Gemini response: {e}")
            return self._create_fallback_response(response_text, claim)
    
    def _create_fallback_response(self, response_text: str, claim: str) -> Dict:
        """Create fallback response when JSON parsing fails."""
        # Try to extract verdict from text
        text_lower = response_text.lower()
        
        if 'false' in text_lower and 'not true' in text_lower:
            verdict = 'FALSE'
            confidence = 70
        elif 'true' in text_lower and 'correct' in text_lower:
            verdict = 'TRUE'
            confidence = 70
        else:
            verdict = 'AMBIGUOUS'
            confidence = 50
        
        return {
            'claim': claim,
            'verdict': verdict,
            'confidence': confidence,
            'explanation': response_text[:500] + "..." if len(response_text) > 500 else response_text,
            'evidence_for': [],
            'evidence_against': [],
            'sources': ['Gemini AI analysis'],
            'context': 'Response parsing failed, showing raw analysis',
            'warnings': ['Response format was not JSON as expected'],
            'related_facts': [],
            'method': 'gemini_ai_fallback',
            'last_updated': 'Unknown',
            'search_terms_used': []
        }
    
    def _create_error_response(self, claim: str, error: str) -> Dict:
        """Create error response."""
        return {
            'claim': claim,
            'verdict': 'AMBIGUOUS',
            'confidence': 25,
            'explanation': f'Analysis failed due to error: {error}',
            'evidence_for': [],
            'evidence_against': [],
            'sources': [],
            'context': 'Error occurred during analysis',
            'warnings': [f'Technical error: {error}'],
            'related_facts': [],
            'method': 'error_response',
            'last_updated': datetime.now().isoformat(),
            'search_terms_used': [],
            'error': error
        }
    
    def test_connection(self) -> Dict:
        """Test Gemini API connection."""
        try:
            response = self.model.generate_content("Hello! Are you working? Please respond with 'Yes, I am working correctly.'")
            return {
                'status': 'success',
                'message': 'Gemini API connection successful',
                'response': response.text,
                'model': 'gemini-1.5-flash'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gemini API connection failed: {str(e)}',
                'error': str(e)
            }
    
    def batch_fact_check(self, claims: List[str]) -> List[Dict]:
        """Batch fact-check multiple claims."""
        results = []
        
        for i, claim in enumerate(claims):
            logger.info(f"Processing claim {i+1}/{len(claims)}: {claim}")
            
            # Use Pro model for complex claims (longer than 100 chars or contains specific keywords)
            use_pro = len(claim) > 100 or any(keyword in claim.lower() 
                                            for keyword in ['medical', 'vaccine', 'climate', 'political'])
            
            result = self.fact_check_claim(claim, use_pro_model=use_pro)
            results.append(result)
        
        return results
    
    def get_usage_info(self) -> Dict:
        """Get information about Gemini usage limits."""
        return {
            'gemini_1_5_flash': {
                'requests_per_minute': 15,
                'requests_per_day': 1500,
                'cost': 'FREE',
                'best_for': 'General fact-checking, high volume'
            },
            'gemini_1_5_pro': {
                'requests_per_minute': 2,
                'requests_per_day': 50,
                'cost': 'FREE',
                'best_for': 'Complex analysis, detailed research'
            },
            'recommendations': [
                'Use Flash model for most fact-checking',
                'Reserve Pro model for complex medical/scientific claims',
                'Consider caching results for repeated claims',
                'Implement rate limiting to stay within quotas'
            ]
        }

def main():
    """Test the Gemini fact checker."""
    print("🚀 Google Gemini Fact Checker for CredLens")
    print("=" * 50)
    
    try:
        checker = GeminiFactChecker()
        
        # Test connection
        print("🔗 Testing Gemini API connection...")
        connection_result = checker.test_connection()
        
        if connection_result['status'] == 'success':
            print("✅ Gemini API connection successful!")
            print(f"Response: {connection_result['response']}")
        else:
            print(f"❌ Connection failed: {connection_result['message']}")
            return
        
        # Show usage info
        usage_info = checker.get_usage_info()
        print(f"\n📊 Gemini Usage Limits:")
        print(f"Flash Model: {usage_info['gemini_1_5_flash']['requests_per_day']} requests/day (FREE)")
        print(f"Pro Model: {usage_info['gemini_1_5_pro']['requests_per_day']} requests/day (FREE)")
        
        # Interactive fact-checking
        print(f"\n💡 Enter claims to fact-check (type 'quit' to exit)")
        print(f"The system will automatically choose Flash or Pro model based on complexity.")
        
        while True:
            try:
                claim = input("\n🔍 Enter claim: ").strip()
                
                if claim.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not claim:
                    continue
                
                print(f"⚡ Analyzing with Gemini AI...")
                result = checker.fact_check_claim(claim)
                
                # Display results
                print(f"\n{'='*60}")
                verdict_icon = {'TRUE': '🟢', 'FALSE': '🔴', 'AMBIGUOUS': '🟡'}.get(result['verdict'], '⚪')
                print(f"{verdict_icon} VERDICT: {result['verdict']} ({result['confidence']}%)")
                print(f"🤖 MODEL: {result.get('model_used', 'gemini-1.5-flash')}")
                print(f"📝 EXPLANATION: {result['explanation']}")
                
                if result.get('evidence_for'):
                    print(f"\n✅ EVIDENCE FOR:")
                    for evidence in result['evidence_for']:
                        print(f"   • {evidence}")
                
                if result.get('evidence_against'):
                    print(f"\n❌ EVIDENCE AGAINST:")
                    for evidence in result['evidence_against']:
                        print(f"   • {evidence}")
                
                if result.get('sources'):
                    print(f"\n📚 SOURCES:")
                    for source in result['sources']:
                        print(f"   • {source}")
                
                if result.get('warnings'):
                    print(f"\n⚠️ WARNINGS:")
                    for warning in result['warnings']:
                        print(f"   • {warning}")
                
                print("=" * 60)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n👋 Thank you for using Gemini Fact Checker!")
        
    except Exception as e:
        print(f"❌ Setup Error: {e}")
        print("\n💡 Setup Instructions:")
        print("1. Install: pip install google-generativeai")
        print("2. Get Gemini API key: https://makersuite.google.com/app/apikey")
        print("3. Add to .env: GEMINI_API_KEY=your_api_key_here")

if __name__ == "__main__":
    main()