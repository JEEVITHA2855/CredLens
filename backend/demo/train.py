import pandas as pd
import os
from model import MisinformationDetector

# Sample training data
TRAINING_DATA = [
    ("Vaccines contain microchips", False),
    ("The Earth revolves around the Sun", True),
    ("5G towers spread COVID-19", False),
    ("Exercise improves health", True),
    ("Water is essential for survival", True),
    ("Climate change is a hoax", False),
    ("The Earth is flat", False),
    ("Smoking causes cancer", True),
    ("Evolution is scientifically proven", True),
    ("The Moon landing was faked", False),
    # Add more training examples
]

def train_model():
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
    
    print("Model training completed successfully!")

if __name__ == "__main__":
    train_model()