"""
Test script for the Industrial Fact Checker
"""
from app.services.industrial_fact_checker import IndustrialFactChecker
import numpy as np
from tabulate import tabulate

def test_industrial_fact_checker():
    """Test the industrial fact checker with different inputs"""
    
    # Initialize the checker
    checker = IndustrialFactChecker()
    
    # Test cases with different expected outcomes
    test_cases = [
        # Claims likely to be true
        "Climate change is a significant global issue caused by human activities",
        "Drinking water is essential for human health and hydration",
        "The speed of light in a vacuum is approximately 299,792,458 meters per second",
        "Regular exercise can help improve cardiovascular health",
        "The Earth orbits around the Sun in our solar system",
        
        # Claims likely to be false
        "5G networks are spreading coronavirus across the world",
        "The Earth is flat and all evidence of a round Earth is fabricated by NASA",
        "COVID-19 vaccines contain microchips to track the population",
        "Climate change is a hoax invented by scientists for grant money",
        "Vaccines cause autism in children",
        
        # Ambiguous or neutral claims
        "Economic growth will increase next year according to some analysts",
        "The stock market may experience volatility in the coming months",
        "Some studies suggest that coffee may have health benefits"
    ]
    
    results = []
    
    # Run tests
    for i, claim in enumerate(test_cases):
        print(f"\nTest {i+1}: '{claim}'")
        print("-" * 60)
        
        result = checker.analyze_misinformation(claim)
        
        print(f"Verdict: {result['verdict']}")
        print(f"Credibility: {result['scores']['overall_credibility']}%")
        print(f"Source Trust: {result['scores']['source_trust']}%")
        print(f"Corroboration: {result['scores']['corroboration']} sources")
        print(f"Contradiction: {result['scores']['contradiction']} sources")
        print(f"Language Safety: {result['scores']['language_safety']}%")
        print(f"Reasoning: {result['reasoning']}")
        
        # Collect results for the summary table
        results.append([
            i+1,
            claim[:40] + "..." if len(claim) > 40 else claim,
            result['verdict'],
            f"{result['scores']['overall_credibility']:.1f}%",
            f"{result['scores']['source_trust']:.1f}%",
            f"{result['scores']['language_safety']:.1f}%"
        ])
    
    # Print summary table
    print("\n\n" + "=" * 80)
    print("INDUSTRIAL FACT CHECKER TEST RESULTS SUMMARY")
    print("=" * 80)
    
    headers = ["#", "Claim", "Verdict", "Credibility", "Source Trust", "Language Safety"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
    
    # Analysis of score distribution
    scores = [float(row[3].replace('%', '')) for row in results]
    
    print(f"\nScore Statistics:")
    print(f"Min Score: {min(scores):.1f}%")
    print(f"Max Score: {max(scores):.1f}%")
    print(f"Mean Score: {np.mean(scores):.1f}%")
    print(f"Standard Deviation: {np.std(scores):.1f}%")
    print(f"Unique Score Count: {len(set(scores))}")
    
    # Validation check
    if len(set(scores)) > len(test_cases) // 2 and max(scores) - min(scores) > 30:
        print("\n✅ SUCCESS: The industrial fact checker is providing dynamic scores!")
        print(f"Score range: {min(scores):.1f}% - {max(scores):.1f}%")
    else:
        print("\n❌ WARNING: The industrial fact checker may still have issues with score variety.")
        print(f"Score range: {min(scores):.1f}% - {max(scores):.1f}%")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_industrial_fact_checker()