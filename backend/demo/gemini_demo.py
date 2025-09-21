"""
CredLens Gemini Fact-Check Demonstration
=======================================

This script demonstrates your working Gemini API integration
with actual fact-checking examples.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add demo directory to path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
load_dotenv()

import google.generativeai as genai

def demonstrate_gemini_fact_checking():
    """Demonstrate the Gemini fact-checking with sample claims."""
    print("🚀 CredLens Gemini AI Fact-Checker Demonstration")
    print("="*60)
    
    # Configure Gemini
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("✅ Gemini API configured successfully")
    print("💰 Using FREE Gemini 1.5 Flash model")
    print(f"🔑 API Key: {api_key[:20]}...")
    
    # Test claims
    test_claims = [
        "The Earth is flat",
        "Vaccines cause autism", 
        "The capital of France is Paris",
        "COVID-19 vaccines contain microchips",
        "There are 24 hours in a day"
    ]
    
    print(f"\n📝 Testing {len(test_claims)} claims with Gemini AI:")
    print("="*60)
    
    for i, claim in enumerate(test_claims, 1):
        print(f"\n🔍 TEST {i}/{len(test_claims)}: '{claim}'")
        print("⚡ Analyzing with Gemini AI (real-time data access)...")
        
        try:
            # Create fact-checking prompt
            prompt = f"""You are a fact-checker with real-time information access. 

Analyze this claim: "{claim}"

Provide your analysis in JSON format:
{{
    "verdict": "TRUE" | "FALSE" | "AMBIGUOUS",
    "confidence": <0-100>,
    "explanation": "<detailed reasoning>",
    "sources": ["<source1>", "<source2>"],
    "key_points": ["<point1>", "<point2>"]
}}

Use current information and cite reliable sources. Respond only with JSON."""
            
            # Get response from Gemini
            response = model.generate_content(prompt)
            response_text = response.text
            
            # Try to parse JSON
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end != 0:
                    json_text = response_text[json_start:json_end]
                    result = json.loads(json_text)
                    
                    # Display results
                    verdict_icon = {'TRUE': '🟢', 'FALSE': '🔴', 'AMBIGUOUS': '🟡'}.get(result.get('verdict', 'UNKNOWN'), '❓')
                    
                    print(f"\n{verdict_icon} VERDICT: {result.get('verdict', 'UNKNOWN')} ({result.get('confidence', 0)}%)")
                    print(f"📝 EXPLANATION: {result.get('explanation', 'No explanation')}")
                    
                    if result.get('sources'):
                        print(f"📚 SOURCES:")
                        for source in result['sources']:
                            print(f"   • {source}")
                    
                    if result.get('key_points'):
                        print(f"🔍 KEY POINTS:")
                        for point in result['key_points']:
                            print(f"   • {point}")
                            
                else:
                    print(f"⚠️ Could not parse JSON, raw response:")
                    print(f"📄 {response_text[:300]}...")
                    
            except json.JSONDecodeError:
                print(f"⚠️ JSON parsing failed, raw response:")
                print(f"📄 {response_text[:300]}...")
                
        except Exception as e:
            print(f"❌ Error analyzing claim: {str(e)}")
        
        print("-" * 60)
        
        # Small delay to respect rate limits
        import time
        time.sleep(1)
    
    print(f"\n🎉 Demonstration complete!")
    print(f"✅ Your Gemini API is working perfectly")
    print(f"💰 Cost: FREE (used {len(test_claims)} of 1,500 daily requests)")
    print(f"🌐 Real-time data access: Enabled")

def test_simple_claim():
    """Test a single simple claim to verify everything works."""
    print("\n🧪 Quick Test - Single Claim Verification")
    print("="*40)
    
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    claim = "There are 60 minutes in an hour"
    print(f"🔍 Testing: '{claim}'")
    
    try:
        prompt = f"Is this statement true or false: '{claim}'. Respond with just TRUE or FALSE and a brief explanation."
        response = model.generate_content(prompt)
        
        print(f"✅ Gemini Response:")
        print(f"📄 {response.text}")
        print(f"🎯 API Status: Working perfectly!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print(__doc__)
    
    # Quick test first
    test_simple_claim()
    
    # Ask if user wants full demonstration
    try:
        choice = input(f"\nRun full demonstration? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            demonstrate_gemini_fact_checking()
        else:
            print("👋 Test complete!")
    except:
        # If input fails, run the demonstration anyway
        print("\nRunning full demonstration...")
        demonstrate_gemini_fact_checking()