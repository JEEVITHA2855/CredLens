"""
Quick test script for individual claims
"""
import sys
sys.path.append('e:/CredLens/backend/demo')

from model import AnalysisModel

def test_claim(claim_text):
    model = AnalysisModel()
    result = model.analyze_text(claim_text)
    
    print(f"\n🔍 CLAIM: '{claim_text}'")
    print(f"📊 SCORE: {result['credibility_score']:.1f}/100")
    print(f"✅ STATUS: {result['verification_status']}")
    print(f"💭 SENTIMENT: {result['sentiment']}")
    print("📋 REASONING:")
    for reason in result['reasoning']:
        print(f"   • {reason}")
    print("📚 SOURCES:")
    for source in result['sources']:
        print(f"   • {source}")
    print("-" * 60)
    
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        claim = " ".join(sys.argv[1:])
        test_claim(claim)
    else:
        # Test some examples
        test_claims = [
            "There are 24 hours in a day",
            "There are 365 days in a year", 
            "Water boils at 100 degrees Celsius",
            "The Earth is flat",
            "Pizza is the best food ever"
        ]
        
        for claim in test_claims:
            test_claim(claim)