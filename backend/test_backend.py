import requests
import json

# Test the backend server
def test_backend():
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test analyze endpoint
    try:
        test_claim = {
            "text": "The Earth is flat and space agencies are lying to us"
        }
        
        response = requests.post(f"{base_url}/analyze", json=test_claim)
        print(f"✅ Analyze endpoint: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📊 Analysis result:")
            print(f"   Status: {result['status']}")
            print(f"   Confidence: {result['confidence_score']:.1%}")
            print(f"   Explanation: {result['explanation'][:100]}...")
            return True
        else:
            print(f"❌ Analysis failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing CredLens Backend API")
    print("=" * 40)
    
    success = test_backend()
    
    if success:
        print("\n🎉 Backend is working properly!")
        print("✅ Your frontend should now be able to connect")
    else:
        print("\n❌ Backend has issues")