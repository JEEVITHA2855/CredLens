"""
Interactive claim analyzer for testing the CredLens system.
"""
from model import AnalysisModel
import json

def pretty_print_result(result):
    """Print analysis results in a readable format."""
    print("\n=== Analysis Results ===")
    print(f"Claim Credibility Score: {result['credibility_score']:.1f}/100")
    print(f"Verification Status: {result['verification_status']}")
    print(f"Sentiment: {result['sentiment']}")
    print("\nReasoning:")
    for reason in result['reasoning']:
        print(f"- {reason}")
    print("\nSources:")
    for source in result['sources']:
        print(f"- {source}")
    print("\nDetailed Results:")
    print(json.dumps(result.get('details', {}), indent=2))
    print("=====================\n")

def main():
    print("CredLens Interactive Claim Analyzer")
    print("Enter a claim to analyze (or 'quit' to exit)")
    
    model = AnalysisModel()
    
    while True:
        try:
            claim = input("\nEnter claim: ").strip()
            if claim.lower() == 'quit':
                break
                
            if not claim:
                print("Please enter a claim to analyze")
                continue
                
            result = model.analyze_text(claim)
            pretty_print_result(result)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()