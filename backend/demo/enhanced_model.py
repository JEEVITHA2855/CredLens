"""
Enhanced CredLens model with advanced AI-powered misinformation detection.
"""
from transformers import pipeline
from scientific_validator import ScientificValidator
from fact_checker import FactCheckAPI
from demo_advanced_detector import DemoAdvancedDetector
import logging
import json

logger = logging.getLogger(__name__)

class EnhancedAnalysisModel:
    def __init__(self):
        # Initialize components
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.scientific_validator = ScientificValidator()
        self.fact_checker = FactCheckAPI()
        self.demo_detector = DemoAdvancedDetector()
        
    def analyze_text(self, text: str, use_advanced: bool = True) -> dict:
        """
        Analyze text with option for advanced AI detection.
        
        Args:
            text: Input text to analyze
            use_advanced: Whether to use the advanced AI detection system
        """
        try:
            # Basic validation
            if not text or not isinstance(text, str):
                return {
                    "error": "Invalid input text",
                    "credibility_score": 0,
                    "sentiment": "neutral",
                    "reasoning": ["Invalid or empty input provided"],
                    "sources": []
                }
            
            if use_advanced:
                # Use demo advanced detection system
                advanced_result = self.demo_detector.analyze(text)
                
                # Convert advanced result to our format
                verdict_to_score = {
                    'TRUE': advanced_result['confidence'],
                    'FALSE': 100 - advanced_result['confidence'],
                    'AMBIGUOUS': max(50, advanced_result['confidence'])
                }
                
                credibility_score = verdict_to_score.get(advanced_result['verdict'], 50)
                
                # Get sentiment for additional context
                sentiment_result = self.sentiment_analyzer(text)[0]
                
                return {
                    "credibility_score": credibility_score,
                    "sentiment": sentiment_result['label'].lower(),
                    "verification_status": advanced_result['verdict'].lower(),
                    "verdict": advanced_result['verdict'],
                    "confidence": advanced_result['confidence'],
                    "reasoning": [
                        advanced_result['explanation'],
                        f"Analysis based on {advanced_result.get('evidence_count', 0)} sources",
                        f"Primary claim: {advanced_result['claim']}"
                    ],
                    "sources": advanced_result.get('sources', []),
                    "advanced_analysis": True,
                    "all_claims": advanced_result.get('all_claims', []),
                    "timestamp": advanced_result.get('timestamp', '')
                }
            else:
                # Fallback to basic analysis
                return self._basic_analysis(text)
                
        except Exception as e:
            logger.error(f"Error in enhanced analysis: {str(e)}")
            # Fallback to basic analysis on error
            return self._basic_analysis(text)
    
    def _basic_analysis(self, text: str) -> dict:
        """Fallback basic analysis method."""
        try:
            # Get comprehensive verification
            verification_results = self._verify_claim(text)
            
            # Get sentiment analysis
            sentiment_result = self.sentiment_analyzer(text)[0]
            
            # Initialize response structure
            sources = []
            reasoning = []
            
            # Process verification results
            if verification_results.get('google_facts', {}).get('found', False):
                sources.extend(['Google Fact Check API'])
                reasoning.append("Verified against fact-checking databases")
                
            if verification_results.get('news_verification', {}).get('found', False):
                sources.extend(['News articles', 'Media reports'])
                reasoning.append("Found corroborating news articles")
                
            if verification_results.get('scientific_validation', {}).get('is_scientific', False):
                sources.extend(verification_results['scientific_validation'].get('sources', []))
                reasoning.append(
                    f"Verified as scientific claim in field: {verification_results['scientific_validation'].get('fact_type', 'general')}"
                )
            
            # Calculate final credibility score
            base_confidence = verification_results.get('aggregate_confidence', 0.5)
            
            # Adjust for sentiment
            sentiment_factor = 0.1 if sentiment_result['label'] == 'POSITIVE' else -0.1
            
            credibility_score = base_confidence * 100 * (1 + sentiment_factor)
            credibility_score = max(0, min(100, credibility_score))
            
            # Add final reasoning points
            if not sources:
                sources = ["AI analysis", "Language pattern detection"]
                reasoning.extend([
                    "No external verification found",
                    f"Sentiment analysis suggests {sentiment_result['label'].lower()} tone"
                ])
            
            return {
                "credibility_score": credibility_score,
                "sentiment": sentiment_result['label'].lower(),
                "verification_status": "unverified",
                "reasoning": reasoning,
                "sources": sources,
                "advanced_analysis": False,
                "details": {
                    "fact_check_results": verification_results.get('google_facts', {}),
                    "news_verification": verification_results.get('news_verification', {}),
                    "scientific_validation": verification_results.get('scientific_validation', {})
                }
            }
            
        except Exception as e:
            logger.error(f"Error in basic analysis: {str(e)}")
            return {
                "error": str(e),
                "credibility_score": 0,
                "sentiment": "neutral",
                "reasoning": ["Error during analysis"],
                "sources": []
            }
    
    def _verify_claim(self, text: str) -> dict:
        """Verify claim using multiple sources."""
        try:
            # Get comprehensive verification from all sources
            verification_results = self.fact_checker.aggregate_verification(text)
            
            # Check if it's a scientific claim
            scientific_result = self.scientific_validator.validate_scientific_claim(text)
            
            if scientific_result['is_scientific']:
                verification_results['scientific_validation'] = scientific_result
                verification_results['aggregate_confidence'] = max(
                    verification_results['aggregate_confidence'],
                    scientific_result['confidence'] / 100
                )
                
            return verification_results
        except Exception as e:
            logger.error(f"Error in claim verification: {str(e)}")
            return {
                'error': str(e),
                'aggregate_confidence': 0.0,
                'verification_count': 0
            }
    
    def batch_analyze(self, texts: list, use_advanced: bool = True) -> list:
        """Analyze multiple texts in batch."""
        results = []
        for text in texts:
            result = self.analyze_text(text, use_advanced=use_advanced)
            results.append(result)
        return results
    
    def get_analysis_summary(self, text: str) -> dict:
        """Get a summary of the analysis capabilities."""
        return {
            "input_length": len(text),
            "has_advanced_detection": True,
            "available_sources": [
                "Wikipedia API",
                "Bing Search API", 
                "Google Fact Check API",
                "Scientific Database",
                "News Verification",
                "Sentiment Analysis"
            ],
            "analysis_methods": [
                "Claim extraction",
                "Evidence retrieval", 
                "Cross-verification",
                "AI reasoning",
                "Confidence scoring"
            ]
        }