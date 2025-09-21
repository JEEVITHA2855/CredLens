"""
Test suite for the Enhanced AI Misinformation Detection System
"""
import sys
sys.path.append('.')
from app.services.enhanced_fact_checker import EnhancedFactChecker

def test_enhanced_system():
    """Test the enhanced AI misinformation detection system"""
    print("\n🔍 ENHANCED AI MISINFORMATION DETECTION SYSTEM TEST")
    print("=" * 70)
    
    checker = EnhancedFactChecker()
    
    test_cases = [
        # Health Claims
        {
            'category': 'HEALTH',
            'input': 'Vaccines have been proven safe through extensive clinical trials',
            'expected': 'TRUE'
        },
        {
            'category': 'HEALTH',
            'input': 'SHOCKING: Vaccines cause autism according to hidden research!',
            'expected': 'FALSE'
        },
        
        # Technology Claims
        {
            'category': 'TECH',
            'input': 'EXPOSED: 5G networks are spreading diseases worldwide!',
            'expected': 'FALSE'
        },
        {
            'category': 'TECH',
            'input': 'Artificial Intelligence models can analyze large datasets efficiently',
            'expected': 'TRUE'
        },
        
        # Scientific Claims
        {
            'category': 'SCIENCE',
            'input': 'The Earth is flat and NASA is hiding the truth!',
            'expected': 'FALSE'
        },
        {
            'category': 'SCIENCE',
            'input': 'The first moon landing occurred in July 1969',
            'expected': 'TRUE'
        },
        
        # Environmental Claims
        {
            'category': 'ENVIRONMENT',
            'input': 'Human activities are contributing to global climate change',
            'expected': 'TRUE'
        },
        {
            'category': 'ENVIRONMENT',
            'input': 'Climate change is a hoax created by China',
            'expected': 'FALSE'
        },
        
        # Complex Claims
        {
            'category': 'COMPLEX',
            'input': 'Studies suggest coffee may have both positive and negative health effects',
            'expected': 'AMBIGUOUS'
        }
    ]
    
    successes = 0
    total = len(test_cases)
    
    for test in test_cases:
        print(f"\n📋 TEST: {test['category']}")
        print("-" * 60)
        print(f"INPUT: {test['input']}")
        print(f"EXPECTED: {test['expected']}")
        print("\nRESULT:")
        
        result = checker.analyze_claim(test['input'])
        
        print(f"Claim: {result['claim']}")
        print(f"Verdict: {result['verdict']}")
        print(f"Reason: {result['reasoning']}")
        print("\nScores:")
        print(f"- Overall Credibility: {result['scores']['overall_credibility']}%")
        print(f"- Source Trust: {result['scores']['source_trust']}%")
        print(f"- Corroboration: {result['scores']['corroboration']} sources")
        print(f"- Contradiction: {result['scores']['contradiction']} sources")
        print(f"- Language Safety: {result['scores']['language_safety']}%")
        
        if result['verdict'] == test['expected']:
            print("\n✅ TEST PASSED")
            successes += 1
        else:
            print(f"\n❌ TEST FAILED - Expected {test['expected']}, got {result['verdict']}")
            
        print(f"Processing Time: {result['processing_time']:.3f}s")
        print(f"Analysis ID: {result['analysis_id']}")
    
    success_rate = (successes / total) * 100
    print("\n📊 TEST SUMMARY:")
    print(f"Total Tests: {total}")
    print(f"Successful: {successes}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    print("\n🔍 SYSTEM CAPABILITIES:")
    print("✓ Real-time analysis without database dependencies")
    print("✓ Semantic understanding of claims")
    print("✓ Knowledge-based verification")
    print("✓ Pattern recognition for misinformation")
    print("✓ Structured scoring system")
    print("✓ Clear reasoning with evidence")

if __name__ == "__main__":
    test_enhanced_system()