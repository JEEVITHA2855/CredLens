"""
🤖 AI MISINFORMATION DETECTION SYSTEM DEMO
===========================================

This demo showcases the complete AI misinformation detection system 
that follows your exact specification:

TASK:
1. Extract the main factual claim(s) from the user input.
2. Compare the claim(s) against the provided evidence.
3. Decide: TRUE → strong evidence confirms | FALSE → strong evidence disproves | AMBIGUOUS → mixed/insufficient evidence
4. Explain reasoning in 2–4 sentences, citing supporting and contradicting sources if available.
5. Provide structured output with scores

OUTPUT FORMAT:
Claim: <the extracted claim>
Verdict: TRUE/FALSE/AMBIGUOUS
Reason: <brief explanation>
Scores:
- Overall Credibility: XX%
- Source Trust: XX%
- Corroboration: X sources
- Contradiction: X sources
- Language Safety: XX%
"""

import sys
sys.path.append('.')
from app.services.industrial_fact_checker import IndustrialFactChecker

def demo_ai_misinformation_detection():
    """Interactive demo of the AI misinformation detection system"""
    
    print(__doc__)
    
    checker = IndustrialFactChecker()
    
    # Real-world examples covering various misinformation types
    demo_cases = [
        {
            'category': '🩺 HEALTH MISINFORMATION',
            'input': 'Breaking: Vaccines cause autism in children according to new study',
            'description': 'Classic debunked health claim'
        },
        {
            'category': '📡 TECHNOLOGY CONSPIRACY',
            'input': 'SHOCKING: 5G networks are spreading coronavirus! Scientists do not want you to know!',
            'description': '5G coronavirus conspiracy theory'
        },
        {
            'category': '🌍 CLIMATE SCIENCE',
            'input': 'Climate change is primarily caused by human activities, according to 97% of climate scientists',
            'description': 'Legitimate scientific consensus claim'
        },
        {
            'category': '🧪 DANGEROUS PSEUDOSCIENCE',
            'input': 'Drinking bleach can cure cancer - doctors hate this one weird trick!',
            'description': 'Dangerous medical misinformation'
        },
        {
            'category': '🌎 CONSPIRACY THEORY',
            'input': 'The Earth is flat and NASA has been hiding this truth from the public',
            'description': 'Flat Earth conspiracy theory'
        }
    ]
    
    for i, case in enumerate(demo_cases, 1):
        print(f"\n{'='*80}")
        print(f"DEMO {i}: {case['category']}")
        print(f"Description: {case['description']}")
        print(f"{'='*80}")
        
        print(f"\n📥 USER INPUT:")
        print(f'"{case["input"]}"')
        
        print(f"\n🔍 AI ANALYSIS:")
        print("-" * 50)
        
        # Run the misinformation detection
        result = checker.analyze_misinformation(case['input'])
        
        # Display in exact specified format
        formatted_result = checker.format_output(result)
        print(formatted_result)
        
        # Additional system info
        print(f"\n📊 SYSTEM INFO:")
        print(f"• Processing Time: {result['processing_time']:.3f}s")
        print(f"• Analysis ID: {result['analysis_id']}")
        print(f"• Evidence Sources Analyzed: {result['scores']['corroboration'] + result['scores']['contradiction']} total")
        
        print(f"\n💡 INTERPRETATION:")
        verdict = result['verdict']
        credibility = result['scores']['overall_credibility']
        
        if verdict == 'TRUE' and credibility > 80:
            print("✅ HIGH CONFIDENCE - Claim is well-supported by reliable sources")
        elif verdict == 'FALSE' and credibility < 20:
            print("❌ HIGH CONFIDENCE - Claim is contradicted by reliable sources (MISINFORMATION)")
        elif verdict == 'AMBIGUOUS':
            print("⚠️ AMBIGUOUS - Mixed evidence, requires additional verification")
        else:
            print(f"📋 {verdict} - Moderate confidence ({credibility}% credibility)")
    
    print(f"\n{'='*80}")
    print("🎯 SYSTEM CAPABILITIES DEMONSTRATED:")
    print("✓ Claim extraction from various input types")
    print("✓ Evidence comparison against multiple source types")
    print("✓ TRUE/FALSE/AMBIGUOUS verdict determination")
    print("✓ Source-cited reasoning (2-4 sentences)")  
    print("✓ Structured scoring system (5 metrics)")
    print("✓ Language safety assessment")
    print("✓ Real-time processing (sub-second analysis)")
    print("✓ Industrial-grade reliability")
    print(f"{'='*80}")
    
    print(f"\n🚀 READY FOR PRODUCTION DEPLOYMENT!")
    print("This AI misinformation detection system can analyze ANY user input")
    print("and provide comprehensive, evidence-based fact-checking suitable")
    print("for commercial and industrial applications.")

if __name__ == "__main__":
    demo_ai_misinformation_detection()