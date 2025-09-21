"""
Test the dynamic scoring in the Industrial Fact Checker
"""
from app.services.industrial_fact_checker import IndustrialFactChecker
import numpy as np
from tabulate import tabulate

def test_dynamic_scoring():
    """Test that the industrial fact checker provides dynamic scores"""
    
    print("Initializing IndustrialFactChecker...")
    checker = IndustrialFactChecker()
    
    # Test cases with different expected outcomes
    test_cases = [
        # Claims likely to be true
        "Vaccines are generally safe and effective",
        "The Earth is round and orbits around the Sun",
        "Research suggests regular exercise improves health",
        "Drinking water is essential for human health",
        "The speed of light in a vacuum is approximately 299,792,458 meters per second",
        
        # Claims likely to be false
        "The Earth is flat according to some theories",
        "5G technology has been proven to cause serious health concerns",
        "COVID-19 vaccines contain microchips to track the population",
        "Climate change is a hoax invented by scientists for grant money",
        "Vaccines cause autism in children",
        
        # Ambiguous or neutral claims
        "Some studies indicate coffee has health benefits",
        "Economic growth will increase next year according to some analysts",
        "The stock market may experience volatility in the coming months"
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
    if len(set(scores)) > len(test_cases) // 2 and max(scores) - min(scores) > 20:
        print("\n✅ SUCCESS: The industrial fact checker is providing dynamic scores!")
        print(f"Score range: {min(scores):.1f}% - {max(scores):.1f}%")
    else:
        print("\n❌ WARNING: The industrial fact checker may still have issues with score variety.")
        print(f"Score range: {min(scores):.1f}% - {max(scores):.1f}%")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_dynamic_scoring()