from app.services.industrial_fact_checker import IndustrialFactChecker
import json
from datetime import datetime

def test_diverse_claims():
    """Test the industrial fact checker with a diverse set of claims"""
    checker = IndustrialFactChecker()
    
    test_claims = [
        # Well-established scientific facts
        "Water boils at 100 degrees Celsius at sea level atmospheric pressure",
        "The Earth completes one rotation on its axis approximately every 24 hours",
        "DNA contains genetic instructions for the development of living things",
        
        # Recent scientific findings with strong evidence
        "mRNA vaccines have been shown to be effective against COVID-19 in multiple clinical trials",
        "Global temperatures have risen by approximately 1.1°C since pre-industrial times",
        "Regular physical exercise is associated with improved cardiovascular health",
        
        # Common misinformation
        "5G networks are responsible for spreading viruses",
        "The Earth is flat and NASA is hiding the truth",
        "Drinking bleach can cure diseases",
        "Ancient civilizations were built by aliens",
        
        # Ambiguous or context-dependent claims
        "Coffee is good for your health",
        "Remote work increases productivity",
        "Artificial intelligence will replace most jobs by 2030",
        
        # Recent events requiring fact-checking
        "Renewable energy is now cheaper than fossil fuels in many countries",
        "Electric vehicles produce zero emissions",
        "Social media use causes depression in teenagers",
        
        # Conspiracy theories
        "The moon landing was faked in a Hollywood studio",
        "There's a secret world government controlling everything",
        "Major historical events were orchestrated by secret societies"
    ]
    
    results = []
    for claim in test_claims:
        print(f"\nAnalyzing claim: {claim}")
        print("-" * 80)
        
        try:
            result = checker.analyze_misinformation(claim)
            results.append({
                'claim': claim,
                'verdict': result['verdict'],
                'credibility_score': result['scores']['overall_credibility'],
                'reasoning': result['reasoning']
            })
            
            # Print analysis results
            print(f"Verdict: {result['verdict']}")
            print(f"Credibility Score: {result['scores']['overall_credibility']}%")
            print(f"Reasoning: {result['reasoning']}")
            
        except Exception as e:
            print(f"Error analyzing claim: {str(e)}")
    
    # Save results to a file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"fact_checker_results_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    test_diverse_claims()