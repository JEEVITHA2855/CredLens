"""
Advanced misinformation detection test suite.
"""
import sys
sys.path.append('e:/CredLens/backend/demo')

from enhanced_model import EnhancedAnalysisModel
import json

def test_advanced_system():
    """Test the advanced AI detection system."""
    print("🚀 CredLens Advanced AI Misinformation Detection System")
    print("=" * 60)
    
    model = EnhancedAnalysisModel()
    
    # Test cases covering different types of claims
    test_cases = [
        # Scientific facts
        {
            "claim": "Vaccines cause autism in children",
            "expected_verdict": "FALSE",
            "category": "Medical Misinformation"
        },
        {
            "claim": "The Earth is round",
            "expected_verdict": "TRUE", 
            "category": "Basic Scientific Fact"
        },
        {
            "claim": "COVID-19 vaccines are effective at preventing severe illness",
            "expected_verdict": "TRUE",
            "category": "Recent Medical Fact"
        },
        # Conspiracy theories
        {
            "claim": "5G towers cause coronavirus",
            "expected_verdict": "FALSE",
            "category": "Conspiracy Theory"
        },
        {
            "claim": "Climate change is a hoax created by scientists",
            "expected_verdict": "FALSE", 
            "category": "Climate Misinformation"
        },
        # Factual statements
        {
            "claim": "Water boils at 100 degrees Celsius at sea level",
            "expected_verdict": "TRUE",
            "category": "Basic Science"
        },
        # Ambiguous or complex claims
        {
            "claim": "Eating chocolate makes you happier",
            "expected_verdict": "AMBIGUOUS",
            "category": "Complex Health Claim"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['category']}")
        print(f"📝 Claim: \"{test_case['claim']}\"")
        print(f"🎯 Expected: {test_case['expected_verdict']}")
        
        try:
            # Test advanced analysis
            result = model.analyze_text(test_case['claim'], use_advanced=True)
            
            print(f"🤖 AI Verdict: {result.get('verdict', 'N/A')}")
            print(f"📊 Confidence: {result.get('confidence', 0)}%")
            print(f"💯 Credibility Score: {result.get('credibility_score', 0):.1f}/100")
            print(f"💭 Explanation: {result.get('reasoning', ['No explanation'])[0]}")
            
            if result.get('sources'):
                print("🔗 Sources:")
                for source in result['sources'][:2]:  # Show first 2 sources
                    print(f"   • {source}")
            
            # Check if verdict matches expectation
            actual_verdict = result.get('verdict', 'UNKNOWN')
            expected = test_case['expected_verdict']
            match_status = "✅ CORRECT" if actual_verdict == expected else "❌ INCORRECT"
            print(f"🏆 Result: {match_status}")
            
            results.append({
                'claim': test_case['claim'],
                'expected': expected,
                'actual': actual_verdict,
                'correct': actual_verdict == expected,
                'confidence': result.get('confidence', 0),
                'category': test_case['category']
            })
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                'claim': test_case['claim'],
                'expected': expected,
                'actual': 'ERROR',
                'correct': False,
                'confidence': 0,
                'category': test_case['category'],
                'error': str(e)
            })
        
        print("-" * 60)
    
    # Summary
    print("\n📈 ANALYSIS SUMMARY")
    print("=" * 60)
    
    correct_count = sum(1 for r in results if r['correct'])
    total_count = len(results)
    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    
    print(f"✅ Correct Predictions: {correct_count}/{total_count}")
    print(f"📊 Overall Accuracy: {accuracy:.1f}%")
    
    # Category breakdown
    categories = {}
    for result in results:
        cat = result['category']
        if cat not in categories:
            categories[cat] = {'correct': 0, 'total': 0}
        categories[cat]['total'] += 1
        if result['correct']:
            categories[cat]['correct'] += 1
    
    print(f"\n📂 Performance by Category:")
    for category, stats in categories.items():
        cat_accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"   {category}: {stats['correct']}/{stats['total']} ({cat_accuracy:.1f}%)")
    
    # Average confidence for correct predictions
    correct_results = [r for r in results if r['correct']]
    if correct_results:
        avg_confidence = sum(r['confidence'] for r in correct_results) / len(correct_results)
        print(f"🎯 Average Confidence (Correct): {avg_confidence:.1f}%")
    
    return results

def interactive_test():
    """Interactive testing interface."""
    print("\n🔧 Interactive Testing Mode")
    print("Enter claims to test (type 'quit' to exit):")
    
    model = EnhancedAnalysisModel()
    
    while True:
        try:
            claim = input("\n📝 Enter claim: ").strip()
            if claim.lower() == 'quit':
                break
            
            if not claim:
                print("Please enter a claim to analyze.")
                continue
            
            print("🔍 Analyzing...")
            result = model.analyze_text(claim, use_advanced=True)
            
            print(f"\n🤖 VERDICT: {result.get('verdict', 'N/A')}")
            print(f"📊 CONFIDENCE: {result.get('confidence', 0)}%")
            print(f"💯 CREDIBILITY: {result.get('credibility_score', 0):.1f}/100")
            print(f"💭 EXPLANATION: {result.get('reasoning', ['No explanation'])[0]}")
            
            if result.get('sources'):
                print("🔗 SOURCES:")
                for i, source in enumerate(result['sources'][:3], 1):
                    print(f"   {i}. {source}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_test()
    else:
        test_advanced_system()