"""
API connectivity test script for CredLens.
Run this after setting up your API keys to verify they work correctly.
"""
import os
import requests
import sys
from datetime import datetime

def test_google_factcheck_api():
    """Test Google Fact Check API."""
    print("🔍 Testing Google Fact Check API...")
    
    api_key = os.getenv('GOOGLE_FACTCHECK_API_KEY')
    if not api_key:
        print("❌ Google Fact Check API key not found in environment variables")
        return False
    
    try:
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {
            'query': 'vaccines cause autism',
            'key': api_key,
            'languageCode': 'en'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            claims_found = len(data.get('claims', []))
            print(f"✅ Google Fact Check API working! Found {claims_found} fact-check claims")
            return True
        elif response.status_code == 403:
            print("❌ Google Fact Check API: Access forbidden. Check API key permissions")
            return False
        else:
            print(f"❌ Google Fact Check API returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Google Fact Check API error: {str(e)}")
        return False

def test_bing_search_api():
    """Test Bing Search API."""
    print("🌐 Testing Bing Search API...")
    
    api_key = os.getenv('BING_SEARCH_API_KEY')
    if not api_key:
        print("❌ Bing Search API key not found in environment variables")
        return False
    
    try:
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {'Ocp-Apim-Subscription-Key': api_key}
        params = {
            'q': 'climate change scientific consensus',
            'count': 5,
            'mkt': 'en-US'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results_count = len(data.get('webPages', {}).get('value', []))
            print(f"✅ Bing Search API working! Found {results_count} web results")
            return True
        elif response.status_code == 401:
            print("❌ Bing Search API: Unauthorized. Check API key")
            return False
        else:
            print(f"❌ Bing Search API returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Bing Search API error: {str(e)}")
        return False

def test_news_api():
    """Test News API."""
    print("📰 Testing News API...")
    
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        print("❌ News API key not found in environment variables")
        return False
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'covid vaccines effectiveness',
            'apiKey': api_key,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 5
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles_count = len(data.get('articles', []))
            print(f"✅ News API working! Found {articles_count} news articles")
            return True
        elif response.status_code == 401:
            print("❌ News API: Unauthorized. Check API key")
            return False
        else:
            print(f"❌ News API returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ News API error: {str(e)}")
        return False

def test_openai_api():
    """Test OpenAI API (optional)."""
    print("🧠 Testing OpenAI API (optional)...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️ OpenAI API key not found (optional)")
        return True  # Not required
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test with a simple completion
        url = "https://api.openai.com/v1/chat/completions"
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': 'Hello, this is a test.'}],
            'max_tokens': 5
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            print("✅ OpenAI API working!")
            return True
        elif response.status_code == 401:
            print("❌ OpenAI API: Unauthorized. Check API key")
            return False
        else:
            print(f"❌ OpenAI API returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API error: {str(e)}")
        return False

def check_environment_file():
    """Check if .env file exists and has required keys."""
    print("📄 Checking environment configuration...")
    
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"❌ .env file not found. Please create {env_file} with your API keys")
        return False
    
    required_keys = [
        'GOOGLE_FACTCHECK_API_KEY',
        'BING_SEARCH_API_KEY', 
        'NEWS_API_KEY'
    ]
    
    missing_keys = []
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing required environment variables: {', '.join(missing_keys)}")
        return False
    
    print("✅ Environment file configured correctly")
    return True

def main():
    """Run all API connectivity tests."""
    print("🚀 CredLens API Connectivity Test")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check environment setup
    if not check_environment_file():
        print("\n❌ Environment setup incomplete. Please follow the API_SETUP_GUIDE.md")
        return False
    
    print()
    
    # Test each API
    tests = [
        ("Google Fact Check API", test_google_factcheck_api),
        ("Bing Search API", test_bing_search_api), 
        ("News API", test_news_api),
        ("OpenAI API", test_openai_api)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            print()
        except Exception as e:
            print(f"❌ Unexpected error testing {name}: {str(e)}")
            results.append((name, False))
            print()
    
    # Summary
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} APIs working correctly")
    
    if passed >= 3:  # At least 3 main APIs working
        print("🎉 Your CredLens setup is ready for advanced misinformation detection!")
        return True
    else:
        print("⚠️ Please fix the failing APIs before using advanced features")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1)