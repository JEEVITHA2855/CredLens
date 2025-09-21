#!/usr/bin/env python3
"""
AI Misinformation Detection System Test
Demonstrates the complete misinformation analysis pipeline
"""

import sys
import os
sys.path.append('.')

from app.services.industrial_fact_checker import IndustrialFactChecker

def test_misinformation_detection():
    """Test the AI misinformation detection system with various claims"""
    
    print("🤖 AI MISINFORMATION DETECTION SYSTEM")
    print("=" * 70)
    print("Testing the complete pipeline following your specification:")
    print("1. Extract main factual claims")
    print("2. Compare against evidence sources") 
    print("3. Decide TRUE/FALSE/AMBIGUOUS")
    print("4. Provide reasoning with source citations")
    print("5. Generate structured scores")
    print("=" * 70)
    
    checker = IndustrialFactChecker()
    
    # Test cases covering different types of misinformation
    test_cases = [
        "Breaking: Vaccines cause autism in children according to new study",
        "COVID-19 vaccines have been shown to be safe and effective through extensive clinical trials",
        "SHOCKING: 5G networks are spreading coronavirus! Scientists do not want you to know!",
        "Climate change is primarily caused by human activities, according to 97% of climate scientists",
        "Drinking bleach can cure cancer - doctors hate this one weird trick!",
        "The Earth is flat and NASA has been hiding this truth from the public"
    ]
    
    for i, user_input in enumerate(test_cases, 1):
        print(f"\n🔍 TEST CASE {i}")
        print(f"USER INPUT: {user_input}")
        print("-" * 50)
        
        try:
            # Run the AI misinformation detection analysis
            result = checker.analyze_misinformation(user_input)
            
            # Display in the exact specified format
            formatted_output = checker.format_output(result)
            print(formatted_output)
            
            # Additional metadata
            print(f"\nProcessing Time: {result['processing_time']:.3f}s")
            print(f"Analysis ID: {result['analysis_id']}")
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
        
        print("=" * 70)
    
    print("\n✅ AI MISINFORMATION DETECTION SYSTEM READY")
    print("📋 This system analyzes ANY user-provided information")
    print("🏭 Suitable for industrial and commercial applications")
    print("🔍 Provides evidence-based verdicts with structured scoring")
    print("⚡ Real-time analysis without database dependencies")

if __name__ == "__main__":
    test_misinformation_detection()