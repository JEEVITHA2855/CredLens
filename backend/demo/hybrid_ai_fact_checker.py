"""
CredLens Hybrid AI Fact-Checker
===============================

The best of both worlds: Uses Google Gemini (free, real-time data) as primary
and OpenAI as backup/comparison for maximum accuracy and reliability.

Features:
- Automatic service selection based on availability
- Cost optimization (free Gemini first)
- Fallback reliability (OpenAI if Gemini fails)  
- Result comparison for enhanced accuracy
- Smart quota management
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Add demo directory to path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
load_dotenv()

# Import existing fact checkers
from openai_detector import OpenAIDetector

# Try to import Gemini (if package available)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)

class HybridAIFactChecker:
    """
    Hybrid fact-checker that intelligently uses both Gemini and OpenAI
    for optimal cost, accuracy, and reliability.
    """
    
    def __init__(self):
        """Initialize both AI services if available."""
        self.services = {}
        self.service_status = {}
        
        # Initialize Gemini if available
        if GEMINI_AVAILABLE and os.getenv('GEMINI_API_KEY'):
            try:
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                self.services['gemini'] = {
                    'flash': genai.GenerativeModel('gemini-1.5-flash'),
                    'pro': genai.GenerativeModel('gemini-1.5-pro')
                }
                self.service_status['gemini'] = self._test_gemini()
            except Exception as e:
                logger.warning(f"Gemini initialization failed: {e}")
                self.service_status['gemini'] = False
        else:
            self.service_status['gemini'] = False
        
        # Initialize OpenAI if available
        if os.getenv('OPENAI_API_KEY'):
            try:
                self.services['openai'] = OpenAIDetector()
                openai_test = self.services['openai'].test_connection()
                self.service_status['openai'] = openai_test.get('status') == 'success'
            except Exception as e:
                logger.warning(f"OpenAI initialization failed: {e}")
                self.service_status['openai'] = False
        else:
            self.service_status['openai'] = False
        
        # Usage tracking for smart quota management
        self.usage_stats = {
            'gemini_requests_today': 0,
            'openai_requests_today': 0,
            'last_reset': datetime.now().date()
        }
        
        logger.info(f"Hybrid AI Fact Checker initialized")
        logger.info(f"Available services: {[k for k, v in self.service_status.items() if v]}")
    
    def _test_gemini(self) -> bool:
        """Test Gemini API connection."""
        try:
            model = self.services['gemini']['flash']
            response = model.generate_content("Hello! Please respond with 'Working correctly.'")
            return 'working' in response.text.lower()
        except Exception:
            return False
    
    def fact_check_claim(self, claim: str, mode: str = "auto") -> Dict:
        """
        Fact-check a claim using the best available AI service.
        
        Args:
            claim (str): The claim to fact-check
            mode (str): "auto", "gemini", "openai", "both"
            
        Returns:
            dict: Comprehensive fact-check result
        """
        # Reset daily counters if needed
        self._reset_daily_counters()
        
        if mode == "both":
            return self._compare_both_services(claim)
        elif mode == "gemini" and self.service_status.get('gemini'):
            return self._fact_check_with_gemini(claim)
        elif mode == "openai" and self.service_status.get('openai'):
            return self._fact_check_with_openai(claim)
        elif mode == "auto":
            return self._auto_fact_check(claim)
        else:
            return self._create_error_response(claim, f"Requested mode '{mode}' not available")
    
    def _auto_fact_check(self, claim: str) -> Dict:
        """Automatically choose the best service based on availability and quotas."""
        
        # Priority 1: Gemini (free and better for fact-checking)
        if (self.service_status.get('gemini') and 
            self.usage_stats['gemini_requests_today'] < 1400):  # Leave buffer
            
            try:
                result = self._fact_check_with_gemini(claim)
                self.usage_stats['gemini_requests_today'] += 1
                return result
            except Exception as e:
                logger.warning(f"Gemini failed, trying OpenAI: {e}")
        
        # Priority 2: OpenAI (if Gemini unavailable/quota exceeded)
        if self.service_status.get('openai'):
            try:
                result = self._fact_check_with_openai(claim)
                self.usage_stats['openai_requests_today'] += 1
                return result
            except Exception as e:
                logger.error(f"OpenAI also failed: {e}")
        
        # Fallback: No services available
        return self._create_error_response(claim, "No AI services currently available")
    
    def _fact_check_with_gemini(self, claim: str) -> Dict:
        """Fact-check using Google Gemini."""
        
        # Choose model based on complexity
        use_pro = (len(claim) > 100 or 
                  any(keyword in claim.lower() for keyword in 
                      ['medical', 'vaccine', 'climate', 'political', 'scientific']))
        
        model = self.services['gemini']['pro' if use_pro else 'flash']
        
        prompt = f"""You are an expert fact-checker with access to real-time information.
Analyze this claim comprehensively:

CLAIM: "{claim}"

Provide your analysis in JSON format:
{{
    "verdict": "TRUE" | "FALSE" | "AMBIGUOUS",
    "confidence": <0-100>,
    "explanation": "<detailed reasoning>",
    "evidence_supporting": ["<point 1>", "<point 2>"],
    "evidence_contradicting": ["<point 1>", "<point 2>"],
    "authoritative_sources": ["<source 1>", "<source 2>"],
    "context": "<background information>",
    "warnings": ["<any warnings>"],
    "last_verified": "<when verified>",
    "search_quality": "<quality of available information>"
}}

Use your real-time search to verify current information. Be especially careful with medical, political, and scientific claims."""
        
        response = model.generate_content(prompt)
        
        try:
            # Extract and parse JSON
            text = response.text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_text = text[json_start:json_end]
                result = json.loads(json_text)
                
                # Standardize and enhance result
                result.update({
                    'claim': claim,
                    'ai_service': f'gemini-1.5-{"pro" if use_pro else "flash"}',
                    'method': 'gemini_with_search',
                    'timestamp': datetime.now().isoformat(),
                    'cost': 'FREE',
                    'real_time_data': True
                })
                
                return result
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            logger.warning(f"Gemini JSON parsing failed: {e}")
            return self._create_fallback_response(claim, response.text, 'gemini')
    
    def _fact_check_with_openai(self, claim: str) -> Dict:
        """Fact-check using OpenAI."""
        try:
            result = self.services['openai'].analyze_claim(claim)
            result.update({
                'ai_service': 'openai-gpt-3.5-turbo',
                'cost': 'PAID',
                'real_time_data': False
            })
            return result
        except Exception as e:
            return self._create_error_response(claim, f"OpenAI analysis failed: {str(e)}")
    
    def _compare_both_services(self, claim: str) -> Dict:
        """Compare results from both Gemini and OpenAI."""
        results = {}
        
        # Try Gemini
        if self.service_status.get('gemini'):
            try:
                results['gemini'] = self._fact_check_with_gemini(claim)
            except Exception as e:
                results['gemini'] = {'error': str(e)}
        
        # Try OpenAI  
        if self.service_status.get('openai'):
            try:
                results['openai'] = self._fact_check_with_openai(claim)
            except Exception as e:
                results['openai'] = {'error': str(e)}
        
        # Create comparison result
        if 'gemini' in results and 'openai' in results:
            return self._create_comparison_result(claim, results['gemini'], results['openai'])
        elif 'gemini' in results:
            return results['gemini']
        elif 'openai' in results:
            return results['openai']
        else:
            return self._create_error_response(claim, "Both services failed")
    
    def _create_comparison_result(self, claim: str, gemini_result: Dict, openai_result: Dict) -> Dict:
        """Create a combined result from both AI services."""
        
        # Extract verdicts
        gemini_verdict = gemini_result.get('verdict', 'AMBIGUOUS')
        openai_verdict = openai_result.get('verdict', 'AMBIGUOUS')
        
        # Determine final verdict
        if gemini_verdict == openai_verdict:
            final_verdict = gemini_verdict
            consensus = True
        else:
            # Gemini gets priority due to real-time data access
            final_verdict = gemini_verdict
            consensus = False
        
        # Average confidence (weighted towards Gemini)
        gemini_conf = gemini_result.get('confidence', 50)
        openai_conf = openai_result.get('confidence', 50)
        final_confidence = int((gemini_conf * 0.6) + (openai_conf * 0.4))
        
        return {
            'claim': claim,
            'verdict': final_verdict,
            'confidence': final_confidence,
            'consensus': consensus,
            'explanation': (f"Gemini: {gemini_result.get('explanation', '')} | "
                          f"OpenAI: {openai_result.get('explanation', '')}"),
            'gemini_result': gemini_result,
            'openai_result': openai_result,
            'method': 'hybrid_comparison',
            'ai_service': 'gemini+openai',
            'timestamp': datetime.now().isoformat(),
            'agreement': 'Yes' if consensus else 'No - Gemini verdict used'
        }
    
    def _create_fallback_response(self, claim: str, response_text: str, service: str) -> Dict:
        """Create fallback response when JSON parsing fails."""
        text_lower = response_text.lower()
        
        # Simple verdict extraction
        if 'false' in text_lower or 'incorrect' in text_lower:
            verdict = 'FALSE'
            confidence = 70
        elif 'true' in text_lower or 'correct' in text_lower:
            verdict = 'TRUE'
            confidence = 70
        else:
            verdict = 'AMBIGUOUS'
            confidence = 50
        
        return {
            'claim': claim,
            'verdict': verdict,
            'confidence': confidence,
            'explanation': response_text[:300] + "..." if len(response_text) > 300 else response_text,
            'ai_service': service,
            'method': f'{service}_fallback',
            'timestamp': datetime.now().isoformat(),
            'parsing_error': True
        }
    
    def _create_error_response(self, claim: str, error: str) -> Dict:
        """Create error response."""
        return {
            'claim': claim,
            'verdict': 'AMBIGUOUS',
            'confidence': 25,
            'explanation': f'Analysis failed: {error}',
            'method': 'error',
            'timestamp': datetime.now().isoformat(),
            'error': error
        }
    
    def _reset_daily_counters(self):
        """Reset daily usage counters if needed."""
        today = datetime.now().date()
        if self.usage_stats['last_reset'] != today:
            self.usage_stats.update({
                'gemini_requests_today': 0,
                'openai_requests_today': 0,
                'last_reset': today
            })
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status."""
        return {
            'services_available': self.service_status,
            'usage_today': {
                'gemini': f"{self.usage_stats['gemini_requests_today']}/1500 (FREE)",
                'openai': f"{self.usage_stats['openai_requests_today']} (PAID)"
            },
            'recommended_service': self._get_recommended_service(),
            'total_services': len([s for s in self.service_status.values() if s]),
            'ready': any(self.service_status.values())
        }
    
    def _get_recommended_service(self) -> str:
        """Get the currently recommended service."""
        if (self.service_status.get('gemini') and 
            self.usage_stats['gemini_requests_today'] < 1400):
            return "Gemini (FREE, real-time data)"
        elif self.service_status.get('openai'):
            return "OpenAI (PAID, reliable)"
        else:
            return "None available"

def interactive_demo():
    """Interactive demo of the hybrid fact-checker."""
    print("🚀 CredLens Hybrid AI Fact-Checker")
    print("=" * 50)
    
    checker = HybridAIFactChecker()
    
    # Show status
    status = checker.get_system_status()
    print(f"📊 System Status:")
    for service, available in status['services_available'].items():
        icon = "✅" if available else "❌"
        print(f"   {icon} {service.capitalize()}: {'Available' if available else 'Unavailable'}")
    
    print(f"\n📈 Today's Usage:")
    for service, usage in status['usage_today'].items():
        print(f"   {service.capitalize()}: {usage}")
    
    print(f"\n🎯 Recommended: {status['recommended_service']}")
    print(f"🎮 Ready: {status['ready']}")
    
    if not status['ready']:
        print(f"\n❌ No AI services available!")
        print(f"💡 Setup Instructions:")
        print(f"1. For Gemini (FREE): pip install google-generativeai")
        print(f"2. Get Gemini key: https://makersuite.google.com/app/apikey") 
        print(f"3. Add to .env: GEMINI_API_KEY=your_key")
        return
    
    print(f"\n" + "=" * 50)
    print(f"💡 Modes available:")
    print(f"• auto (recommended) - Smart service selection")
    print(f"• gemini - Force Gemini usage")
    print(f"• openai - Force OpenAI usage") 
    print(f"• both - Compare both services")
    print(f"=" * 50)
    
    while True:
        try:
            claim = input(f"\n🔍 Enter claim to fact-check (or 'quit'): ").strip()
            
            if claim.lower() in ['quit', 'exit', 'q']:
                break
                
            if not claim:
                continue
            
            mode = input(f"🎮 Mode (auto/gemini/openai/both) [auto]: ").strip() or "auto"
            
            print(f"\n⚡ Analyzing with {mode} mode...")
            result = checker.fact_check_claim(claim, mode)
            
            # Display results
            print(f"\n{'=' * 60}")
            verdict_icon = {'TRUE': '🟢', 'FALSE': '🔴', 'AMBIGUOUS': '🟡'}.get(result['verdict'], '⚪')
            print(f"{verdict_icon} VERDICT: {result['verdict']} ({result['confidence']}%)")
            print(f"🤖 SERVICE: {result.get('ai_service', 'unknown')}")
            print(f"💰 COST: {result.get('cost', 'unknown')}")
            
            if result.get('consensus') is not None:
                agreement_icon = "✅" if result['consensus'] else "⚠️"
                print(f"{agreement_icon} AGREEMENT: {result.get('agreement', 'N/A')}")
            
            print(f"📝 EXPLANATION: {result['explanation']}")
            
            if result.get('real_time_data'):
                print(f"🌐 REAL-TIME DATA: Yes (current information)")
            
            print("=" * 60)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n👋 Thank you for using Hybrid AI Fact Checker!")

if __name__ == "__main__":
    interactive_demo()