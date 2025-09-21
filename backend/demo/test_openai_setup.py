"""
Test OpenAI integration setup without making API calls.
"""
import os
import sys
import json
from pathlib import Path

# Add the demo directory to Python path
sys.path.append(str(Path(__file__).parent))

from openai_detector import OpenAIDetector
from scientific_validator import ScientificValidator

def test_setup():
    """Test that all components are properly configured."""
    print("🔧 Testing CredLens OpenAI Integration Setup...")
    print("=" * 50)
    
    # Check environment variables
    print("\n📋 Checking Environment Configuration:")
    api_key = os.getenv('OPENAI_API_KEY')
    model_name = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
    
    print(f"✓ OPENAI_API_KEY: {'Set (' + api_key[:20] + '...)' if api_key else '❌ Not set'}")
    print(f"✓ MODEL_NAME: {model_name}")
    print(f"✓ TEMPERATURE: {os.getenv('TEMPERATURE', '0.3')}")
    print(f"✓ MAX_TOKENS: {os.getenv('MAX_TOKENS', '1000')}")
    
    # Check OpenAI package
    print("\n📦 Checking Package Installation:")
    try:
        import openai
        print(f"✓ OpenAI package: v{openai.__version__}")
        print(f"✓ API Key configured: {'Yes' if hasattr(openai, 'api_key') and openai.api_key else 'No'}")
    except ImportError as e:
        print(f"❌ OpenAI package: Not installed ({e})")
        return False
    
    # Test detector initialization
    print("\n🤖 Testing Detector Initialization:")
    try:
        detector = OpenAIDetector()
        print("✓ OpenAIDetector: Successfully initialized")
        print(f"✓ Model: {detector.model}")
        print(f"✓ Temperature: {detector.temperature}")
        print(f"✓ Max tokens: {detector.max_tokens}")
    except Exception as e:
        print(f"❌ OpenAIDetector: Failed to initialize ({e})")
        return False
    
    # Test scientific validator
    print("\n🔬 Testing Scientific Validator:")
    try:
        validator = ScientificValidator()
        print("✓ ScientificValidator: Successfully initialized")
        
        # Test with sample claim
        test_claim = "Vaccines are safe and effective"
        result = validator.validate_scientific_claim(test_claim)
        print(f"✓ Sample validation: {result.get('verdict', 'N/A')}")
    except Exception as e:
        print(f"❌ ScientificValidator: Failed ({e})")
        return False
    
    # Test prompt generation
    print("\n📝 Testing Prompt Generation:")
    try:
        detector = OpenAIDetector()
        system_prompt = detector._get_system_prompt()
        analysis_prompt = detector._create_analysis_prompt("Test claim")
        
        print(f"✓ System prompt: {len(system_prompt)} characters")
        print(f"✓ Analysis prompt: {len(analysis_prompt)} characters")
        
        # Show sample prompts
        print("\n📄 Sample System Prompt Preview:")
        print(system_prompt[:200] + "..." if len(system_prompt) > 200 else system_prompt)
        
    except Exception as e:
        print(f"❌ Prompt generation: Failed ({e})")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Setup Test Complete!")
    print("\n📝 Next Steps:")
    print("1. Ensure you have a valid OpenAI API key with available quota")
    print("2. Update your .env file with the working API key")
    print("3. Run 'python test_openai.py' to test live API functionality")
    print("4. Consider getting API keys for:")
    print("   - Google Fact Check API")
    print("   - News API")
    print("   - Bing Search API")
    
    return True

if __name__ == "__main__":
    test_setup()