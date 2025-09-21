"""
CredLens API Keys Setup Guide
============================

This guide will help you obtain all the API keys needed for comprehensive 
misinformation detection with CredLens.

Current Status:
✅ OpenAI API: Configured (needs quota/valid key)
🔑 Google Fact Check API: Needed
🔑 News API: Needed  
🔑 Bing Search API: Needed

"""

# API Keys Setup Instructions

## 1. OpenAI API Key (REQUIRED)
"""
Status: ⚠️  Configured but quota exceeded

Steps to get/fix OpenAI API key:
1. Visit: https://platform.openai.com/api-keys
2. Create account or log in
3. Click "Create new secret key"
4. Copy the key (starts with sk-proj- or sk-)
5. Add billing information at: https://platform.openai.com/account/billing
6. Purchase credits or set up payment method
7. Update .env file: OPENAI_API_KEY=your_new_key_here

Cost: $0.002 per 1K tokens (very affordable for testing)
Free tier: $5 in free credits for new accounts
"""

## 2. Google Fact Check Tools API (RECOMMENDED)
"""
Purpose: Access to Google's fact-checking database
Cost: Free up to 1,000 requests/day

Steps:
1. Go to: https://console.developers.google.com/
2. Create a new project or select existing
3. Enable "Fact Check Tools API"
4. Go to Credentials → Create Credentials → API Key
5. Restrict the key to Fact Check Tools API
6. Update .env: GOOGLE_FACTCHECK_API_KEY=your_api_key

Documentation: https://developers.google.com/fact-check/tools/api/
"""

## 3. News API (RECOMMENDED)
"""
Purpose: Access to news articles for fact verification
Cost: Free tier (1,000 requests/day), paid plans available

Steps:
1. Visit: https://newsapi.org/register
2. Create free account
3. Verify email
4. Get API key from dashboard
5. Update .env: NEWS_API_KEY=your_api_key

Documentation: https://newsapi.org/docs
"""

## 4. Bing Web Search API (OPTIONAL)
"""
Purpose: Additional web search capabilities for fact checking
Cost: Free tier (1,000 transactions/month)

Steps:
1. Visit: https://portal.azure.com/
2. Create Azure account (free)
3. Create "Bing Search v7" resource
4. Go to Keys and Endpoint
5. Copy Key 1
6. Update .env: BING_SEARCH_API_KEY=your_api_key

Documentation: https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/
"""

# Testing Your Setup

def test_all_apis():
    """
    Once you have obtained the API keys, run this test to verify everything works:
    
    1. Update your .env file with all keys
    2. Run: python backend/demo/test_openai.py
    3. Run: python backend/demo/test_all_apis.py (create this file)
    
    Expected results:
    - OpenAI: Should analyze claims with AI reasoning
    - Google Fact Check: Should find fact-checked claims
    - News API: Should retrieve relevant news articles  
    - Bing Search: Should provide web search results
    """
    pass

# Priority Order for API Keys

"""
For best results, obtain keys in this order:

1. CRITICAL - OpenAI API Key
   - Core AI-powered analysis
   - Advanced reasoning capabilities
   - Required for intelligent misinformation detection

2. HIGH - Google Fact Check Tools API  
   - Access to verified fact-checked claims
   - Free and reliable
   - Adds authoritative source verification

3. MEDIUM - News API
   - Current news context
   - Article verification
   - Helps with recent claims

4. LOW - Bing Search API
   - Additional search capabilities
   - Backup verification source
   - More comprehensive web coverage
"""

if __name__ == "__main__":
    print(__doc__)
    print("\n🔑 API Keys Setup Priority:")
    print("1. ⚠️  Fix OpenAI API key (quota/billing)")
    print("2. 🆓 Get Google Fact Check API key (free)")
    print("3. 🆓 Get News API key (free tier)")
    print("4. 🌐 Get Bing Search API key (optional)")
    print("\nRun this file for detailed instructions!")