"""
CredLens Live Demo - See What Your System Does! 🚀
================================================

This demo shows exactly what happens when someone uses CredLens
to fact-check claims in real-time.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add demo directory to path
sys.path.append(str(Path(__file__).parent))

def simulate_credlens_usage():
    """
    Simulates a user interacting with CredLens through the web interface
    """
    print("🌐 CredLens Web Interface Simulation")
    print("="*50)
    print("User opens: http://localhost:3000/credlens")
    print()
    
    # Simulate user interaction
    claims_to_test = [
        "The COVID-19 vaccine contains microchips",
        "There are 24 hours in a day", 
        "Drinking bleach can cure diseases",
        "The Earth revolves around the Sun"
    ]
    
    for i, claim in enumerate(claims_to_test, 1):
        print(f"📝 USER TYPES: '{claim}'")
        print("🔄 User clicks 'Analyze Claim' button...")
        print()
        
        # Show the processing steps
        print("⚡ CREDLENS PROCESSING:")
        print("├── 🔬 Checking scientific database...")
        print("├── 🤖 Sending to OpenAI for AI analysis...")
        print("├── 📰 Searching Google Fact Check database...")
        print("├── 🌐 Searching recent news articles...")
        print("├── 🔍 Performing web search for sources...")
        print("└── 🧠 Aggregating results...")
        print()
        
        # Show results based on claim type
        if "microchip" in claim.lower():
            show_false_result(claim)
        elif "24 hours" in claim:
            show_true_result(claim)
        elif "bleach" in claim.lower():
            show_dangerous_false_result(claim)
        else:
            show_true_result(claim)
            
        print("─"*50)
        if i < len(claims_to_test):
            input("Press Enter to see next example...")
        print()

def show_false_result(claim):
    """Shows what a FALSE verdict looks like"""
    print("🔴 RESULT DISPLAY:")
    print(f"   Claim: {claim}")
    print("   📊 VERDICT: FALSE")
    print("   🎯 CONFIDENCE: 97%")
    print("   📝 EXPLANATION: No evidence supports the presence of microchips in")
    print("      COVID-19 vaccines. This claim has been debunked by multiple")
    print("      fact-checkers and health organizations worldwide.")
    print()
    print("   📚 SOURCES:")
    print("   • ✅ Reuters Fact Check: 'COVID-19 vaccines do not contain microchips'")  
    print("   • ✅ CDC Official Statement: 'Vaccine ingredients publicly available'")
    print("   • ✅ WHO Myth-busting: 'No tracking devices in vaccines'")
    print("   • ✅ Snopes: 'FALSE - No microchips in vaccines'")
    print()
    print("   🔬 ANALYSIS BREAKDOWN:")
    print("   • AI Reasoning: FALSE (98% confidence)")
    print("   • Fact Checkers: FALSE (4 sources)")  
    print("   • Scientific Database: No matches")
    print("   • Web Sources: 15 authoritative debunks")

def show_true_result(claim):
    """Shows what a TRUE verdict looks like"""
    print("🟢 RESULT DISPLAY:")
    print(f"   Claim: {claim}")
    print("   📊 VERDICT: TRUE")
    print("   🎯 CONFIDENCE: 100%")
    print("   📝 EXPLANATION: This is a verified scientific fact. A day is defined")
    print("      as the time it takes for Earth to complete one full rotation")
    print("      on its axis, which is 24 hours.")
    print()
    print("   📚 SOURCES:")
    print("   • ✅ Scientific Database: Direct match found")
    print("   • ✅ NASA: 'Earth's rotation period'")
    print("   • ✅ Encyclopedia Britannica: 'Definition of a day'")  
    print("   • ✅ International Bureau of Weights and Measures")
    print()
    print("   🔬 ANALYSIS BREAKDOWN:")
    print("   • Scientific Database: TRUE (100% match)")
    print("   • AI Reasoning: TRUE (100% confidence)")
    print("   • Fact Checkers: No articles needed (basic fact)")
    print("   • Web Sources: Universal agreement")

def show_dangerous_false_result(claim):
    """Shows what a dangerous FALSE claim looks like"""
    print("🔴 RESULT DISPLAY:")
    print(f"   Claim: {claim}")
    print("   📊 VERDICT: FALSE")
    print("   🎯 CONFIDENCE: 99%")
    print("   ⚠️  WARNING: POTENTIALLY HARMFUL MISINFORMATION")
    print("   📝 EXPLANATION: Drinking bleach is extremely dangerous and can cause")
    print("      severe chemical burns, organ damage, and death. It has no medical")
    print("      benefits and should never be consumed.")
    print()
    print("   🚨 HEALTH WARNING:")
    print("   • ☎️  If consumed, contact Poison Control immediately")
    print("   • 🏥 Seek emergency medical attention")
    print("   • 📞 US Poison Control: 1-800-222-1222")
    print()
    print("   📚 SOURCES:")
    print("   • ✅ CDC Warning: 'Bleach consumption extremely dangerous'")
    print("   • ✅ FDA Alert: 'Do not consume bleach products'")
    print("   • ✅ Mayo Clinic: 'Chemical poisoning symptoms'")
    print("   • ✅ WHO: 'Bleach not safe for human consumption'")

def show_web_interface_features():
    """Shows what the web interface looks like"""
    print("\n🖥️  CREDLENS WEB INTERFACE FEATURES:")
    print("="*50)
    print("🎯 HOME PAGE:")
    print("   • Large text input box: 'Enter claim to fact-check...'")
    print("   • 'Analyze Claim' button")
    print("   • Recent fact-checks history")
    print("   • Usage statistics")
    print()
    print("📊 RESULTS PAGE:")
    print("   • Large verdict badge (GREEN/RED/YELLOW)")
    print("   • Confidence meter (0-100%)")
    print("   • Detailed explanation paragraph")
    print("   • Expandable source list")
    print("   • 'Share Result' button")
    print("   • 'Fact-check Another' button")
    print()
    print("🔍 ADVANCED FEATURES:")
    print("   • Batch upload (multiple claims)")
    print("   • Export results (PDF/JSON)")
    print("   • API access dashboard")
    print("   • Analytics and trends")

def show_api_usage():
    """Shows how developers can use the API"""
    print("\n🔌 API USAGE EXAMPLE:")
    print("="*50)
    print("POST /api/fact-check")
    print("Content-Type: application/json")
    print()
    print('{"claim": "Vaccines cause autism"}')
    print()
    print("📤 RESPONSE:")
    print("""{
  "verdict": "FALSE",
  "confidence": 98,
  "explanation": "Multiple studies found no link...",
  "sources": [
    {"title": "CDC Study", "url": "...", "credibility": "HIGH"},
    {"title": "Cochrane Review", "url": "...", "credibility": "HIGH"}
  ],
  "processing_time": "2.3 seconds",
  "timestamp": "2025-09-20T10:30:45Z"
}""")

def main():
    """Run the complete CredLens demo"""
    print(__doc__)
    
    print("🎮 WHAT YOU'RE ABOUT TO SEE:")
    print("• How users interact with CredLens")
    print("• What results look like")  
    print("• How the system processes different claim types")
    print("• Web interface features")
    print()
    
    input("Press Enter to start the demo...")
    print()
    
    # Main demo
    simulate_credlens_usage()
    
    # Show interface features
    show_web_interface_features()
    
    # Show API usage
    show_api_usage()
    
    print("\n" + "="*50)
    print("✅ DEMO COMPLETE!")
    print()
    print("🎯 YOUR CREDLENS SYSTEM:")
    print("• Fights misinformation with AI + multiple sources")
    print("• Provides transparent, confidence-scored results")  
    print("• Offers both web interface and API access")
    print("• Handles medical, scientific, political, and general claims")
    print("• Warns about dangerous misinformation")
    print()
    print("🚀 READY TO LAUNCH:")
    print("1. Get working OpenAI API key")
    print("2. Start backend: python backend/app.py")
    print("3. Start frontend: npm start")
    print("4. Open: http://localhost:3000")
    print("5. Start fact-checking! 🛡️")

if __name__ == "__main__":
    main()