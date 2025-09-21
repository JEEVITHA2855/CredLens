import requests
import json

def test_backend_api():
    """Test the running backend API"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing CredLens Backend API")
    print("=" * 40)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health Check: {response.status_code}")
        print(f"📄 Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test analyze endpoint with a sample claim
    print("\n🔍 Testing Analysis Endpoint")
    print("-" * 30)
    
    test_claim = {
        "text": "The moon landing was faked by NASA"
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze", 
            json=test_claim,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis Status: {response.status_code}")
            print(f"📊 Result: {result['status']}")
            print(f"🎯 Confidence: {result['confidence_score']:.1%}")
            print(f"💭 Explanation: {result['explanation'][:150]}...")
            print(f"📚 Evidence Count: {len(result.get('evidence', []))}")
            
            print(f"\n🎉 Backend API is working perfectly!")
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"📄 Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Analysis request failed: {e}")

if __name__ == "__main__":
    test_backend_api()