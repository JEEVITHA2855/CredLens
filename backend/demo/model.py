from transformers import pipeline
from scientific_validator import ScientificValidator
from fact_checker import FactCheckAPI
import logging

logger = logging.getLogger(__name__)

class AnalysisModel:
    def __init__(self):
        # Initialize components
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.scientific_validator = ScientificValidator()
        self.fact_checker = FactCheckAPI()

    def verify_claim(self, text):
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

    def analyze_text(self, text):
        """Analyze text using multiple verification sources and sentiment analysis."""
        try:
            # Basic sanitization
            if not text or not isinstance(text, str):
                return {
                    "error": "Invalid input text",
                    "credibility_score": 0,
                    "sentiment": "neutral",
                    "reasoning": ["Invalid or empty input provided"],
                    "sources": []
                }

            # Get comprehensive verification
            verification_results = self.verify_claim(text)
            
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
                "verification_status": "unverified",  # Default to unverified in demo mode
                "reasoning": reasoning,
                "sources": sources,
                "details": {
                    "fact_check_results": verification_results.get('google_facts', {}),
                    "news_verification": verification_results.get('news_verification', {}),
                    "scientific_validation": verification_results.get('scientific_validation', {})
                }
            }
            
        except Exception as e:
            logger.error(f"Error in text analysis: {str(e)}")
            return {
                "error": str(e),
                "credibility_score": 0,
                "sentiment": "neutral",
                "reasoning": ["Error during analysis"],
                "sources": []
            }