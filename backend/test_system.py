#!/usr/bin/env python3
"""
Simple test script to verify CredLens system components
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing system imports...")
    
    try:
        from app.models.database import db
        print("✅ Database module loaded")
        
        from app.services.claim_extractor import ClaimExtractor
        print("✅ Claim extractor loaded")
        
        from app.services.retriever import SemanticRetriever
        print("✅ Semantic retriever loaded")
        
        from app.services.verifier import NLIVerifier
        print("✅ NLI verifier loaded")
        
        from app.services.credibility_scorer import CredibilityScorer
        print("✅ Credibility scorer loaded")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("\n🗄️ Testing database...")
    
    try:
        from app.models.database import db
        
        # Initialize database
        db.init_db()
        print("✅ Database initialized")
        
        # Get fact checks
        fact_checks = db.get_all_fact_checks()
        print(f"✅ Found {len(fact_checks)} fact checks in database")
        
        if fact_checks:
            sample = fact_checks[0]
            print(f"   Sample: {sample.claim[:60]}...")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_ai_services():
    """Test AI service initialization"""
    print("\n🤖 Testing AI services...")
    
    try:
        from app.services.claim_extractor import ClaimExtractor
        from app.services.verifier import NLIVerifier
        from app.services.credibility_scorer import CredibilityScorer
        
        # Test claim extractor
        extractor = ClaimExtractor()
        claim = extractor.extract_from_text("The COVID-19 vaccine is safe and effective.")
        print(f"✅ Claim extraction: Extracted claim: {claim[:50]}...")
        
        # Test NLI verifier (this loads the model)
        print("   Loading NLI model...")
        verifier = NLIVerifier()
        print("✅ NLI verifier initialized")
        
        # Test credibility scorer
        scorer = CredibilityScorer()
        print("✅ Credibility scorer initialized")
        
        return True
    except Exception as e:
        print(f"❌ AI services error: {e}")
        return False

if __name__ == "__main__":
    print("🔥 CredLens System Test")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test database
    if success and not test_database():
        success = False
    
    # Test AI services
    if success and not test_ai_services():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! CredLens system is ready.")
        print("\n🚀 To start the system:")
        print("   Backend:  python run.py")
        print("   Frontend: npm start (in frontend directory)")
    else:
        print("❌ Some tests failed. Please check the errors above.")