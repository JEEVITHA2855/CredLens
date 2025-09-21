"""
Test OpenAI-powered misinformation detection system.
"""
import sys
sys.path.append('e:/CredLens/backend/demo')

from openai_detector import OpenAIDetector
import json

def test_openai_connection():
    """Test OpenAI API connection."""
    print("🔗 Testing OpenAI API Connection...")
    print("=" * 50)
    
    detector = OpenAIDetector()
    result = detector.test_connection()
    
    if result['status'] == 'success':
        print("✅ OpenAI API Connection: SUCCESS")
        print(f"🤖 Model: {result['model']}")
        print(f"💬 Test Response: {result['response']}")
        return True
    else:
        print("❌ OpenAI API Connection: FAILED")
        print(f"🚨 Error: {result['message']}")
        return False

def test_misinformation_detection():
    """Test misinformation detection with various claims."""
    print("\n🧠 Testing OpenAI Misinformation Detection")
    print("=" * 50)
    
    detector = OpenAIDetector()
    
    test_cases = [
        {
            "claim": "Vaccines cause autism in children",
            "expected": "FALSE",
            "category": "Medical Misinformation"
        },
        {
            "claim": "The Earth revolves around the Sun",
            "expected": "TRUE",
            "category": "Basic Science"
        },
        {
            "claim": "Climate change is caused by human activities",
            "expected": "TRUE", 
            "category": "Climate Science"
        },
        {
            "claim": "5G towers cause COVID-19",
            "expected": "FALSE",
            "category": "Conspiracy Theory"
        },
        {
            "claim": "Water freezes at 0 degrees Celsius",
            "expected": "TRUE",
            "category": "Basic Science"
        },
        {
            "claim": "The moon landing was faked by NASA",
            "expected": "FALSE",
            "category": "Historical Conspiracy"
        },
        {
            "claim": "Eating carrots improves night vision significantly",
            "expected": "AMBIGUOUS",
            "category": "Health Myth"
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test['category']}")
        print(f"📝 Claim: \"{test['claim']}\"")
        print(f"🎯 Expected: {test['expected']}")
        
        try:
            result = detector.analyze_claim(test['claim'])
            
            print(f"🤖 AI Verdict: {result['verdict']}")
            print(f"📊 Confidence: {result['confidence']}%")
            print(f"🔬 Method: {result['method']}")
            print(f"💭 Explanation: {result['explanation']}")
            
            if result.get('reasoning_steps'):
                print("🧮 Reasoning Steps:")
                for step in result['reasoning_steps'][:2]:  # Show first 2 steps
                    print(f"   • {step}")
            
            # Check accuracy
            is_correct = result['verdict'] == test['expected']
            status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
            print(f"🏆 Result: {status}")
            
            results.append({
                'claim': test['claim'],
                'expected': test['expected'],
                'actual': result['verdict'],
                'confidence': result['confidence'],
                'correct': is_correct,
                'method': result['method'],
                'category': test['category']
            })
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                'claim': test['claim'],
                'expected': test['expected'],
                'actual': 'ERROR',
                'confidence': 0,
                'correct': False,
                'error': str(e),
                'category': test['category']
            })
        
        print("-" * 60)
    
    # Summary
    print("\n📈 PERFORMANCE SUMMARY")
    print("=" * 60)
    
    correct_count = sum(1 for r in results if r['correct'])
    total_count = len(results)
    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    
    print(f"✅ Correct Predictions: {correct_count}/{total_count}")
    print(f"📊 Overall Accuracy: {accuracy:.1f}%")
    
    # Method breakdown
    methods = {}
    for result in results:
        method = result.get('method', 'unknown')
        if method not in methods:
            methods[method] = {'correct': 0, 'total': 0}
        methods[method]['total'] += 1
        if result['correct']:
            methods[method]['correct'] += 1
    
    print(f"\n🔬 Performance by Method:")
    for method, stats in methods.items():
        method_accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"   {method}: {stats['correct']}/{stats['total']} ({method_accuracy:.1f}%)")
    
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
    """Interactive testing mode."""
    print("\n🔧 Interactive OpenAI Testing Mode")
    print("Enter claims to analyze (type 'quit' to exit):")
    
    detector = OpenAIDetector()
    
    while True:
        try:
            claim = input("\n📝 Enter claim: ").strip()
            if claim.lower() == 'quit':
                break
            
            if not claim:
                print("Please enter a claim to analyze.")
                continue
            
            print("🧠 Analyzing with OpenAI...")
            result = detector.analyze_claim(claim)
            
            print(f"\n🤖 VERDICT: {result['verdict']}")
            print(f"📊 CONFIDENCE: {result['confidence']}%")
            print(f"💭 EXPLANATION: {result['explanation']}")
            print(f"🔬 METHOD: {result['method']}")
            
            if result.get('reasoning_steps'):
                print("🧮 REASONING STEPS:")
                for i, step in enumerate(result['reasoning_steps'], 1):
                    print(f"   {i}. {step}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Test connection first
    if test_openai_connection():
        if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
            interactive_test()
        else:
            test_misinformation_detection()
    else:
        print("\n❌ Cannot proceed with testing due to API connection failure.")
        print("\nPlease check your OpenAI API key and try again.")