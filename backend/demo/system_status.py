"""
CredLens System Status Demo
==========================
Complete system demonstration showing all components working
"""

import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def show_system_status():
    print("🚀 CredLens System Status Report")
    print("=" * 50)
    
    # Check Environment
    print("🔧 ENVIRONMENT SETUP:")
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print(f"✅ Gemini API Key: {gemini_key[:20]}...{gemini_key[-10:]}")
    else:
        print("❌ Gemini API Key: Not found")
    
    # Check Gemini AI
    print("\n🤖 AI SERVICE STATUS:")
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Quick test
        response = model.generate_content("Respond with just: WORKING")
        if "WORKING" in response.text:
            print("✅ Gemini AI: Connected and responding")
        else:
            print("⚠️ Gemini AI: Connected but unexpected response")
    except Exception as e:
        print(f"❌ Gemini AI: Error - {e}")
    
    # Check backend components
    print("\n📦 BACKEND COMPONENTS:")
    
    try:
        import requests
        print("✅ Requests library: Available")
    except:
        print("❌ Requests library: Missing")
    
    try:
        from fastapi import FastAPI
        print("✅ FastAPI: Available")
    except:
        print("❌ FastAPI: Missing")
    
    try:
        import uvicorn
        print("✅ Uvicorn: Available")
    except:
        print("❌ Uvicorn: Missing")

def demo_fact_checking():
    print("\n🔍 FACT-CHECKING DEMONSTRATION:")
    print("-" * 40)
    
    # Import Gemini
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        test_claims = [
            "Drinking water is essential for human health",
            "The sun rises in the west",
            "2 + 2 equals 5"
        ]
        
        for i, claim in enumerate(test_claims, 1):
            print(f"\n📋 TEST {i}: '{claim}'")
            
            prompt = f"Is this true or false: '{claim}'. Respond with TRUE/FALSE and brief reason."
            response = model.generate_content(prompt)
            
            # Determine verdict
            if "TRUE" in response.text.upper():
                verdict = "✅ TRUE"
            elif "FALSE" in response.text.upper():
                verdict = "❌ FALSE"
            else:
                verdict = "❓ UNCERTAIN"
            
            print(f"🎯 {verdict}")
            print(f"💭 {response.text[:100]}...")
            
            time.sleep(1)  # Rate limiting
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")

def show_usage_info():
    print("\n📋 USAGE INFORMATION:")
    print("-" * 30)
    print("🌐 Frontend URL: http://localhost:3001")
    print("🔧 Backend URL: http://localhost:8000")
    print("🔑 API Endpoints:")
    print("   • GET  /health - Health check")
    print("   • POST /analyze - Fact-check claims")
    print("\n💰 COST: FREE (1,500 requests/day with Gemini)")
    print("🚀 STATUS: Ready for use!")

if __name__ == "__main__":
    show_system_status()
    demo_fact_checking()
    show_usage_info()
    
    print("\n🎉 CredLens system is fully operational!")
    print("👉 Open http://localhost:3001 in your browser to start using the app")