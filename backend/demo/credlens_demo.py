"""
CredLens Integration Demo - Shows how all components work together
================================================================

This demo shows how CredLens combines OpenAI reasoning with multiple fact-checking
sources to provide comprehensive misinformation detection.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add demo directory to path
sys.path.append(str(Path(__file__).parent))

from openai_detector import OpenAIDetector
from scientific_validator import ScientificValidator

class CredLensDemo:
    """Demonstrates the full CredLens fact-checking pipeline."""
    
    def __init__(self):
        self.openai_detector = OpenAIDetector()
        self.scientific_validator = ScientificValidator()
        
    def analyze_claim_comprehensive(self, claim):
        """
        Comprehensive claim analysis using multiple methods.
        This is what CredLens does with all APIs working.
        """
        print(f"🔍 Analyzing: '{claim}'\n")
        
        results = {
            "claim": claim,
            "timestamp": datetime.now().isoformat(),
            "analyses": {}
        }
        
        # 1. Scientific Validation (local database)
        print("1. 🔬 Scientific Database Check...")
        scientific_result = self.scientific_validator.validate_scientific_claim(claim)
        results["analyses"]["scientific"] = scientific_result
        
        if scientific_result.get("matches"):
            print(f"   ✓ Found scientific match: {scientific_result['verdict']}")
            print(f"   📊 Confidence: {scientific_result.get('confidence', 0)}%")
        else:
            print("   ➜ No direct scientific match found")
        
        # 2. OpenAI Analysis (when API key works)
        print("\n2. 🤖 AI Reasoning Analysis...")
        try:
            # This would work with valid OpenAI API key
            ai_result = self.simulate_openai_analysis(claim)
            results["analyses"]["openai"] = ai_result
            print(f"   ✓ AI Analysis: {ai_result['verdict']}")
            print(f"   🧠 Reasoning: {ai_result['explanation'][:100]}...")
        except Exception as e:
            print(f"   ❌ AI Analysis unavailable: {str(e)}")
            results["analyses"]["openai"] = {"error": str(e)}
        
        # 3. Google Fact Check (simulated)
        print("\n3. 📰 Google Fact Check Database...")
        fact_check_result = self.simulate_fact_check_search(claim)
        results["analyses"]["fact_check"] = fact_check_result
        
        if fact_check_result.get("found_articles"):
            print(f"   ✓ Found {len(fact_check_result['articles'])} fact-check articles")
            for article in fact_check_result["articles"][:2]:
                print(f"   📄 {article['title']} - {article['rating']}")
        else:
            print("   ➜ No fact-check articles found")
        
        # 4. News Context (simulated)  
        print("\n4. 📰 Recent News Context...")
        news_result = self.simulate_news_search(claim)
        results["analyses"]["news"] = news_result
        print(f"   ✓ Found {len(news_result['articles'])} relevant news articles")
        
        # 5. Web Search (simulated)
        print("\n5. 🌐 Web Search Verification...")
        web_result = self.simulate_web_search(claim)
        results["analyses"]["web_search"] = web_result
        print(f"   ✓ Found {len(web_result['results'])} web sources")
        
        # 6. Final Verdict Aggregation
        print("\n📊 Aggregating Results...")
        final_verdict = self.aggregate_verdicts(results["analyses"])
        results["final_verdict"] = final_verdict
        
        print(f"\n{'='*60}")
        print(f"🎯 FINAL VERDICT: {final_verdict['verdict']}")
        print(f"📊 CONFIDENCE: {final_verdict['confidence']}%")
        print(f"🔍 METHOD: {final_verdict['primary_method']}")
        print(f"📝 EXPLANATION: {final_verdict['explanation']}")
        print(f"{'='*60}")
        
        return results
    
    def simulate_openai_analysis(self, claim):
        """Simulates what OpenAI would return (for demo purposes)."""
        # This simulates the type of analysis OpenAI would provide
        mock_responses = [
            {
                "keywords": ["earth", "flat"],
                "response": {
                    "verdict": "FALSE",
                    "confidence": 99,
                    "explanation": "The claim that Earth is flat contradicts centuries of scientific evidence. Earth is an oblate spheroid, as demonstrated by satellite imagery, physics of gravity, and astronomical observations.",
                    "reasoning": "Scientific consensus, empirical evidence",
                    "sources_needed": ["NASA imagery", "gravitational physics", "shipping routes"]
                }
            },
            {
                "keywords": ["vaccine", "autism"],
                "response": {
                    "verdict": "FALSE", 
                    "confidence": 98,
                    "explanation": "Multiple large-scale studies have found no causal link between vaccines and autism. The original study making this claim was retracted due to fraud.",
                    "reasoning": "Meta-analysis of medical studies",
                    "sources_needed": ["CDC studies", "retracted Wakefield study", "autism prevalence data"]
                }
            },
            {
                "keywords": ["24", "hours", "day"],
                "response": {
                    "verdict": "TRUE",
                    "confidence": 100,
                    "explanation": "A day is defined as 24 hours, consisting of one full rotation of Earth on its axis.",
                    "reasoning": "Scientific definition, astronomical measurement",
                    "sources_needed": ["astronomical data", "time measurement standards"]
                }
            },
            {
                "keywords": ["coffee", "health"],
                "response": {
                    "verdict": "AMBIGUOUS",
                    "confidence": 65,
                    "explanation": "Research shows coffee has both benefits (antioxidants, reduced disease risk) and drawbacks (anxiety, sleep disruption). Effects vary by individual and consumption amount.",
                    "reasoning": "Mixed scientific evidence",
                    "sources_needed": ["nutritional studies", "cardiovascular research", "caffeine effects"]
                }
            }
        ]
        
        # Find best match
        claim_lower = claim.lower()
        for mock in mock_responses:
            if any(keyword in claim_lower for keyword in mock["keywords"]):
                return mock["response"]
                
        return {
            "verdict": "AMBIGUOUS",
            "confidence": 50,
            "explanation": "Claim requires additional context and evidence for accurate assessment.",
            "reasoning": "Insufficient information for definitive analysis",
            "sources_needed": ["scholarly articles", "expert opinions", "empirical data"]
        }
    
    def simulate_fact_check_search(self, claim):
        """Simulates Google Fact Check API results."""
        # Mock fact-check database
        fact_checks = [
            {
                "claim": "earth is flat",
                "articles": [
                    {"title": "Fact Check: Is the Earth Flat?", "rating": "FALSE", "source": "Snopes"},
                    {"title": "Debunking Flat Earth Claims", "rating": "PANTS ON FIRE", "source": "PolitiFact"}
                ]
            },
            {
                "claim": "vaccines cause autism",
                "articles": [
                    {"title": "Do Vaccines Cause Autism?", "rating": "FALSE", "source": "FactCheck.org"},
                    {"title": "The Vaccine-Autism Link Myth", "rating": "FALSE", "source": "Reuters"}
                ]
            }
        ]
        
        for fact_check in fact_checks:
            if any(word in claim.lower() for word in fact_check["claim"].split()):
                return {
                    "found_articles": True,
                    "articles": fact_check["articles"],
                    "source": "Google Fact Check API"
                }
        
        return {"found_articles": False, "articles": [], "source": "Google Fact Check API"}
    
    def simulate_news_search(self, claim):
        """Simulates News API results."""
        return {
            "articles": [
                {"title": f"Recent developments related to: {claim[:50]}...", "relevance": 85},
                {"title": f"Expert opinion on: {claim[:50]}...", "relevance": 78},
                {"title": f"Scientific study examines: {claim[:50]}...", "relevance": 72}
            ],
            "source": "News API"
        }
    
    def simulate_web_search(self, claim):
        """Simulates Bing Search API results."""
        return {
            "results": [
                {"title": f"Wikipedia: {claim[:50]}...", "credibility": "HIGH"},
                {"title": f"Academic research on: {claim[:50]}...", "credibility": "HIGH"},
                {"title": f"News article: {claim[:50]}...", "credibility": "MEDIUM"},
                {"title": f"Blog post about: {claim[:50]}...", "credibility": "LOW"}
            ],
            "source": "Bing Search API"
        }
    
    def aggregate_verdicts(self, analyses):
        """Combines all analysis results into final verdict."""
        # This is where CredLens's intelligence shines - smart aggregation
        verdicts = []
        confidences = []
        
        # Collect verdicts from each analysis
        for method, result in analyses.items():
            if isinstance(result, dict) and "verdict" in result:
                verdicts.append(result["verdict"])
                confidences.append(result.get("confidence", 50))
        
        # Smart aggregation logic
        if not verdicts:
            return {
                "verdict": "AMBIGUOUS",
                "confidence": 25,
                "primary_method": "none",
                "explanation": "Insufficient data for analysis"
            }
        
        # Count verdict types
        false_count = verdicts.count("FALSE")
        true_count = verdicts.count("TRUE")
        ambiguous_count = verdicts.count("AMBIGUOUS")
        
        # Determine final verdict
        if false_count > true_count and false_count > ambiguous_count:
            final_verdict = "FALSE"
            avg_confidence = sum(c for i, c in enumerate(confidences) if verdicts[i] == "FALSE") // false_count
        elif true_count > false_count and true_count > ambiguous_count:
            final_verdict = "TRUE"  
            avg_confidence = sum(c for i, c in enumerate(confidences) if verdicts[i] == "TRUE") // true_count
        else:
            final_verdict = "AMBIGUOUS"
            avg_confidence = sum(confidences) // len(confidences)
        
        return {
            "verdict": final_verdict,
            "confidence": min(avg_confidence, 95),  # Cap at 95% to show uncertainty
            "primary_method": "aggregated_analysis",
            "explanation": f"Based on {len(verdicts)} analysis methods, with {false_count} FALSE, {true_count} TRUE, and {ambiguous_count} AMBIGUOUS verdicts."
        }

def main():
    """Run comprehensive fact-checking demo."""
    demo = CredLensDemo()
    
    print("🚀 CredLens Comprehensive Fact-Checking Demo")
    print("=" * 60)
    print("This demo shows how CredLens would work with all API keys configured.\n")
    
    # Test claims
    test_claims = [
        "The Earth is flat",
        "Vaccines cause autism", 
        "There are 24 hours in a day",
        "Coffee is good for your health"
    ]
    
    for i, claim in enumerate(test_claims, 1):
        print(f"\n{'='*20} TEST {i}/{len(test_claims)} {'='*20}")
        demo.analyze_claim_comprehensive(claim)
        
        if i < len(test_claims):
            input("\nPress Enter to continue to next test...")
    
    print(f"\n{'='*60}")
    print("✅ Demo Complete!")
    print("\n💡 Next Steps:")
    print("1. Get valid OpenAI API key with quota")
    print("2. Obtain other API keys (see api_keys_guide.py)")
    print("3. Test with real APIs using test_openai.py")
    print("4. Integrate into main CredLens application")

if __name__ == "__main__":
    main()