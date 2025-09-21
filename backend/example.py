"""
Example script demonstrating how to use the enhanced IndustrialFactChecker
with ML-based misinformation detection.
"""
import os
import json
import os
import sys
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from credlens.ml.setup import EnvironmentSetup
from credlens.ml.model import MisinformationModel
from credlens.ml.prediction import get_prediction_service
from credlens.ml.vertex_ai import initialize_vertex_ai
from credlens.services.industrial_fact_checker import IndustrialFactChecker

def train_and_evaluate_model(training_data_path):
    """Train and evaluate the model using the provided training data."""
    # Load and prepare the data
    data = pd.read_csv(training_data_path)
    X = data['text']  # Assuming 'text' is the column containing the article text
    y = data['label']  # Assuming 'label' is the column containing the labels
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Initialize and train the model
    model = MisinformationModel()
    model.train(X_train, y_train)
    
    # Evaluate the model
    evaluation_report = model.evaluate(X_test, y_test)
    
    return model, evaluation_report

def setup_environment():
    """Set up the Google Cloud environment"""
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'app', 'ml', 'config', 'ml_config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    # Initialize environment setup
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        raise ValueError(
            "Please set GOOGLE_APPLICATION_CREDENTIALS environment variable " +
            "to point to your Google Cloud service account key file"
        )
        
    setup = EnvironmentSetup(credentials_path)
    if not setup.validate_credentials():
        raise ValueError("Invalid Google Cloud credentials")
        
    setup.setup_environment(
        config['project_id'],
        config['bucket_name'],
        config['location']
    )
    
def train_and_deploy_model(training_data_path):
    """Train and deploy the ML model"""
    # Train model
    model = MisinformationModel()
    model, evaluation = train_and_evaluate_model(training_data_path)
    print("\nModel Evaluation:")
    print(evaluation)
    
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'app', 'ml', 'config', 'ml_config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Save model to Cloud Storage
    model.save_model(config['bucket_name'], f"models/{config['model_name']}/{config['model_version']}")
    
    # Deploy to Vertex AI
    from app.ml.vertex_ai import initialize_vertex_ai
    vertex_manager = initialize_vertex_ai(config['project_id'])
    
    model_uri = f"gs://{config['bucket_name']}/models/{config['model_name']}/{config['model_version']}"
    model, endpoint = vertex_manager.deploy_model(
        model_uri,
        config['model_name']
    )
    
    print(f"\nModel deployed successfully to endpoint: {endpoint.name}")
    
def analyze_claim(claim):
    """Analyze a claim using the enhanced fact checker"""
    # Initialize fact checker
    fact_checker = IndustrialFactChecker()
    
    # Analyze the claim
    analysis = fact_checker.analyze_misinformation(claim)
    
    # Print results
    print("\nAnalysis Results:")
    print("-" * 50)
    print(f"Claim: {claim}")
    print(f"\nCredibility Score: {analysis['credibility_score']:.1f}%")
    print(f"Confidence Level: {analysis['confidence_level']}")
    print(f"\nReasoning:")
    print(analysis['reasoning'])
    
    if 'ml_analysis' in analysis:
        print("\nML Model Analysis:")
        print(f"ML Credibility Score: {analysis['ml_analysis']['credibility_score']:.1f}%")
        print(f"ML Confidence Level: {analysis['ml_analysis']['confidence_level']}")
        print(f"ML Classification: {analysis['ml_analysis']['classification']}")
    
    print("\nEvidence:")
    for evidence in analysis['evidence']['supporting']:
        print(f"✓ {evidence['summary']}")
    for evidence in analysis['evidence']['contradicting']:
        print(f"✗ {evidence['summary']}")
    
    return analysis

if __name__ == "__main__":
    # Example usage
    try:
        # Set up environment
        setup_environment()
        
        # Example claims to analyze
        claims = [
            "COVID-19 vaccines contain microchips for tracking people",
            "Regular exercise and a balanced diet can help improve overall health",
            "5G networks are responsible for spreading coronavirus",
            "The Earth is flat and NASA is hiding the truth",
        ]
        
        # Analyze each claim
        for claim in claims:
            print("\n" + "="*80)
            analyze_claim(claim)
            
    except Exception as e:
        print(f"Error: {str(e)}")