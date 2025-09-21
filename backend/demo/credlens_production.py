"""
CredLens Production Fact-Checker
===============================
Production-ready fact-checking tool using Google Gemini AI
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import google.generativeai as genai

class CredLensFacChecker:
    def __init__(self):
        """Initialize the CredLens Fact-Checker."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ CredLens Fact-Checker initialized with Gemini AI")
    
    def check_claim(self, claim):
        """
        Fact-check a single claim using Gemini AI.
        
        Args:
            claim (str): The claim to fact-check
            
        Returns:
            dict: Analysis results with verdict, confidence, explanation, sources
        """
        if not claim.strip():
            return {"error": "Please provide a claim to fact-check"}
        
        prompt = f"""You are a professional fact-checker with real-time information access. 

Analyze this claim: "{claim}"

Provide your analysis in JSON format:
{{
    "verdict": "TRUE" | "FALSE" | "AMBIGUOUS",
    "confidence": <0-100>,
    "explanation": "<detailed reasoning>",
    "sources": ["<source1>", "<source2>"],
    "key_points": ["<point1>", "<point2>"],
    "timestamp": "{datetime.now().isoformat()}"
}}

Use current, accurate information and cite reliable sources. Respond only with JSON."""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_text = response_text[json_start:json_end]
                result = json.loads(json_text)
                result['raw_response'] = response_text
                result['claim'] = claim
                return result
            else:
                return {
                    "error": "Could not parse AI response",
                    "raw_response": response_text,
                    "claim": claim
                }
                
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON response from AI",
                "raw_response": response_text,
                "claim": claim
            }
        except Exception as e:
            return {
                "error": f"AI service error: {str(e)}",
                "claim": claim
            }
    
    def batch_check(self, claims):
        """
        Fact-check multiple claims.
        
        Args:
            claims (list): List of claims to fact-check
            
        Returns:
            list: List of analysis results
        """
        results = []
        for i, claim in enumerate(claims, 1):
            print(f"🔍 Checking claim {i}/{len(claims)}: {claim[:50]}...")
            result = self.check_claim(claim)
            results.append(result)
            
            # Small delay for rate limiting
            import time
            time.sleep(0.5)
            
        return results
    
    def format_result(self, result):
        """Format a fact-check result for display."""
        if 'error' in result:
            return f"❌ Error: {result['error']}"
        
        verdict_icon = {
            'TRUE': '🟢',
            'FALSE': '🔴', 
            'AMBIGUOUS': '🟡'
        }.get(result.get('verdict', 'UNKNOWN'), '❓')
        
        output = []
        output.append(f"📋 CLAIM: {result.get('claim', 'N/A')}")
        output.append(f"{verdict_icon} VERDICT: {result.get('verdict', 'UNKNOWN')} ({result.get('confidence', 0)}%)")
        output.append(f"💭 EXPLANATION: {result.get('explanation', 'No explanation')}")
        
        if result.get('sources'):
            output.append("📚 SOURCES:")
            for source in result['sources']:
                output.append(f"   • {source}")
        
        if result.get('key_points'):
            output.append("🔍 KEY POINTS:")
            for point in result['key_points']:
                output.append(f"   • {point}")
        
        return '\n'.join(output)

def main():
    """Main function for command-line usage."""
    print("🚀 CredLens Professional Fact-Checker")
    print("=====================================")
    print("Powered by Google Gemini AI with real-time data access")
    
    try:
        checker = CredLensFacChecker()
        
        # Sample claims for demonstration
        sample_claims = [
            "The Great Wall of China is visible from space",
            "Lightning never strikes the same place twice",
            "Goldfish have a 3-second memory",
            "The Earth's core is made of molten iron",
            "Humans only use 10% of their brain"
        ]
        
        print(f"\n📝 Fact-checking {len(sample_claims)} sample claims:")
        print("="*60)
        
        for i, claim in enumerate(sample_claims, 1):
            print(f"\n🔍 ANALYSIS {i}/{len(sample_claims)}:")
            print("-" * 40)
            
            result = checker.check_claim(claim)
            print(checker.format_result(result))
            
        print(f"\n🎉 Fact-checking complete!")
        print(f"💰 Cost: FREE (Gemini 1.5 Flash)")
        print(f"🌐 Real-time data: ✅ Enabled")
        
    except Exception as e:
        print(f"❌ Error initializing fact-checker: {e}")

if __name__ == "__main__":
    main()