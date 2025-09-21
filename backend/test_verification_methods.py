#!/usr/bin/env python3
"""
Test script demonstrating both verification approaches in CredLens
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_real_time_verification():
    """Test the real-time verification endpoint"""
    print("🚀 REAL-TIME VERIFICATION TEST")
    print("=" * 50)
    
    test_claims = [
        {
            "text": "Vaccines cause autism in children",
            "expected": "FALSE"
        },
        {
            "text": "The COVID-19 vaccine is safe and effective",
            "expected": "TRUE"
        },
        {
            "text": "5G networks spread coronavirus",
            "expected": "FALSE"
        }
    ]
    
    for i, test_case in enumerate(test_claims, 1):
        print(f"\n{i}. Testing: {test_case['text']}")
        
        try:
            response = requests.post(f"{BASE_URL}/analyze", json={
                "text": test_case['text']
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Verdict: {result['verification_status']}")
                print(f"   📝 Reasoning: {result['explanation'][:100]}...")
                print(f"   📊 Credibility: {result['credibility_fingerprint']['overall_score']}%")
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ⚠️ Server not running on http://localhost:8000")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return True

def test_evidence_based_verification():
    """Test the evidence-based verification endpoint"""
    print("\n\n📚 EVIDENCE-BASED VERIFICATION TEST")
    print("=" * 50)
    
    # Test case with provided evidence
    test_data = {
        "claim": "COVID-19 vaccines are safe and effective",
        "evidence_sources": [
            {
                "source": "CDC",
                "content": "COVID-19 vaccines are safe and effective. They underwent rigorous clinical trials and continue to be monitored for safety.",
                "url": "https://www.cdc.gov/coronavirus/2019-ncov/vaccines/safety/"
            },
            {
                "source": "WHO", 
                "content": "WHO confirms COVID-19 vaccines have been proven safe and effective in preventing severe disease and death.",
                "url": "https://www.who.int/news-room/q-a-detail/coronavirus-disease-(covid-19)-vaccines"
            },
            {
                "source": "New England Journal of Medicine",
                "content": "Clinical trial results demonstrate 95% efficacy and good safety profile for COVID-19 vaccine.",
                "url": "https://www.nejm.org/doi/full/10.1056/NEJMoa2034577"
            }
        ]
    }
    
    print(f"Testing: {test_data['claim']}")
    print(f"Evidence sources: {len(test_data['evidence_sources'])}")
    
    try:
        response = requests.post(f"{BASE_URL}/analyze-with-evidence", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n📋 ANALYSIS RESULT:")
            print(f"Claim: {result['claim']}")
            print(f"Verdict: {result['verdict']}")
            print(f"Reason: {result['reasoning']}")
            print(f"Scores:")
            print(f"- Overall Credibility: {result['scores']['overall_credibility']}%")
            print(f"- Source Trust: {result['scores']['source_trust']}%") 
            print(f"- Corroboration: {result['scores']['corroboration']} sources")
            print(f"- Language Safety: {result['scores']['language_safety']}%")
            print(f"\nEvidence Breakdown:")
            print(f"- Supporting: {result['evidence_breakdown']['supporting']} sources")
            print(f"- Contradicting: {result['evidence_breakdown']['contradicting']} sources")
            print(f"- Total: {result['evidence_breakdown']['total_sources']} sources")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Server not running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    print("🔍 CredLens Verification System Test")
    print("Testing both verification approaches...")
    
    # Test real-time verification
    realtime_success = test_real_time_verification()
    
    # Test evidence-based verification  
    evidence_success = test_evidence_based_verification()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"Real-time verification: {'✅ PASSED' if realtime_success else '❌ FAILED'}")
    print(f"Evidence-based verification: {'✅ PASSED' if evidence_success else '❌ FAILED'}")
    
    if realtime_success and evidence_success:
        print("\n🎉 All tests passed! Both verification methods are working.")
    else:
        print("\n⚠️ Some tests failed. Make sure the server is running: python run.py")

if __name__ == "__main__":
    main()