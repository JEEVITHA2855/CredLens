from model import MisinformationDetector
from data import TRAINING_DATA
import pandas as pd
import os

def main():
    # Create model directory
    model_dir = "saved_model"
    os.makedirs(model_dir, exist_ok=True)
    
    # Prepare training data
    texts, labels = zip(*TRAINING_DATA)
    
    # Initialize and train model
    print("Training model...")
    detector = MisinformationDetector()
    detector.train(texts, labels)
    
    # Save the model
    print("Saving model...")
    detector.save_model(model_dir)
    
    # Test some examples
    test_claims = [
        "Vaccines contain microchips that track your location",
        "Regular exercise can improve your overall health",
        "5G towers are spreading COVID-19",
        "The Earth is a spheroid shape",
        "Drinking water is essential for human survival"
    ]
    
    print("\nAnalyzing test claims...")
    print("-" * 80)
    
    for claim in test_claims:
        result = detector.analyze_text(claim)
        
        print(f"\nClaim: {result['text']}")
        print(f"Classification: {result['classification']}")
        print(f"Credibility Score: {result['credibility_score']}%")
        print(f"Confidence Level: {result['confidence_level']}")
        print(f"Confidence Score: {result['confidence_score']}%")
        print(f"Probabilities:")
        print(f"  - Credible: {result['probabilities']['credible']}%")
        print(f"  - Misinformation: {result['probabilities']['misinformation']}%")
        print("-" * 80)

if __name__ == "__main__":
    main()