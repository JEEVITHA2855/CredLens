"""
OpenAI-powered misinformation detection with advanced reasoning capabilities.
"""
import os
import json
import logging
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv
import openai
from scientific_validator import ScientificValidator

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class OpenAIDetector:
    """Advanced misinformation detector using OpenAI GPT models."""
    
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
        self.temperature = float(os.getenv('TEMPERATURE', 0.3))
        self.max_tokens = int(os.getenv('MAX_TOKENS', 1000))
        self.scientific_validator = ScientificValidator()
        
    def analyze_claim(self, claim: str) -> Dict:
        """Analyze a claim using OpenAI's advanced reasoning."""
        try:
            # First check our scientific validator for known facts
            scientific_result = self.scientific_validator.validate_scientific_claim(claim)
            
            if scientific_result['is_scientific']:
                return {
                    "claim": claim,
                    "verdict": "TRUE",
                    "confidence": scientific_result['confidence'],
                    "explanation": f"Scientific fact verified: {scientific_result.get('reference', '')}",
                    "sources": scientific_result['sources'],
                    "method": "scientific_validation",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Use OpenAI for advanced analysis
            prompt = self._create_analysis_prompt(claim)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Parse OpenAI response
            ai_analysis = response.choices[0].message["content"]
            result = self._parse_ai_response(ai_analysis, claim)
            
            return result
            
        except Exception as e:
            logger.error(f"OpenAI analysis error: {str(e)}")
            return {
                "claim": claim,
                "verdict": "AMBIGUOUS",
                "confidence": 25,
                "explanation": f"Analysis failed: {str(e)}",
                "sources": [],
                "method": "error_fallback",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _get_system_prompt(self) -> str:
        """System prompt for OpenAI analysis."""
        return """You are an expert fact-checker and misinformation detection AI. Your task is to analyze claims and determine their veracity.

For each claim, provide:
1. VERDICT: TRUE, FALSE, or AMBIGUOUS
2. CONFIDENCE: A percentage (0-100) indicating certainty
3. EXPLANATION: Clear reasoning for your verdict
4. EVIDENCE_TYPE: The type of evidence considered (scientific, historical, logical, etc.)

Guidelines:
- TRUE: Claim is factually accurate and well-supported
- FALSE: Claim contradicts established facts or evidence
- AMBIGUOUS: Insufficient evidence or partially true/controversial

Be objective and base your analysis on:
- Scientific consensus
- Historical facts
- Logical reasoning
- Credible sources

Respond in JSON format."""
    
    def _create_analysis_prompt(self, claim: str) -> str:
        """Create analysis prompt for the claim."""
        return f"""Analyze this claim for misinformation:

CLAIM: "{claim}"

Please provide a comprehensive fact-check analysis in JSON format with these fields:
- verdict: "TRUE", "FALSE", or "AMBIGUOUS"
- confidence: integer from 0-100
- explanation: detailed reasoning (2-3 sentences)
- evidence_type: type of evidence used
- reasoning_steps: array of logical steps taken
- potential_sources: array of source types that would verify this

Focus on accuracy and provide clear reasoning."""
    
    def _parse_ai_response(self, ai_response: str, claim: str) -> Dict:
        """Parse OpenAI response into structured format."""
        try:
            # Try to extract JSON from the response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = ai_response[start_idx:end_idx]
                parsed = json.loads(json_str)
                
                return {
                    "claim": claim,
                    "verdict": parsed.get('verdict', 'AMBIGUOUS'),
                    "confidence": min(100, max(0, parsed.get('confidence', 50))),
                    "explanation": parsed.get('explanation', 'No explanation provided'),
                    "evidence_type": parsed.get('evidence_type', 'AI analysis'),
                    "reasoning_steps": parsed.get('reasoning_steps', []),
                    "sources": parsed.get('potential_sources', ['AI analysis']),
                    "method": "openai_analysis",
                    "timestamp": datetime.now().isoformat(),
                    "raw_response": ai_response
                }
            else:
                # Fallback parsing if JSON is not found
                return self._fallback_parse(ai_response, claim)
                
        except json.JSONDecodeError:
            return self._fallback_parse(ai_response, claim)
    
    def _fallback_parse(self, response: str, claim: str) -> Dict:
        """Fallback parsing when JSON parsing fails."""
        response_lower = response.lower()
        
        # Determine verdict based on keywords
        if 'false' in response_lower or 'incorrect' in response_lower or 'myth' in response_lower:
            verdict = 'FALSE'
            confidence = 70
        elif 'true' in response_lower or 'correct' in response_lower or 'accurate' in response_lower:
            verdict = 'TRUE'
            confidence = 70
        else:
            verdict = 'AMBIGUOUS'
            confidence = 50
        
        return {
            "claim": claim,
            "verdict": verdict,
            "confidence": confidence,
            "explanation": response[:200] + "..." if len(response) > 200 else response,
            "sources": ["AI analysis"],
            "method": "openai_fallback",
            "timestamp": datetime.now().isoformat(),
            "raw_response": response
        }
    
    def test_connection(self) -> Dict:
        """Test OpenAI API connection."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello, are you working?"}],
                max_tokens=50
            )
            
            return {
                "status": "success",
                "message": "OpenAI API connection successful",
                "model": self.model,
                "response": response.choices[0].message["content"]
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"OpenAI API connection failed: {str(e)}",
                "error": str(e)
            }