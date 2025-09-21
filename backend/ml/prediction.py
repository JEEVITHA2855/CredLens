from google.cloud import aiplatform
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Union
import json

class PredictionService:
    def __init__(self, project_id: str, endpoint_id: str, location: str = "us-central1"):
        """Initialize the prediction service.
        
        Args:
            project_id (str): Google Cloud project ID
            endpoint_id (str): Vertex AI endpoint ID
            location (str): Google Cloud region
        """
        self.project_id = project_id
        self.endpoint_id = endpoint_id
        self.location = location
        self.endpoint = aiplatform.Endpoint(endpoint_id)
        
    def predict_text(
        self, 
        text: Union[str, List[str]]
    ) -> Tuple[List[int], List[List[float]]]:
        """Get predictions for text content.
        
        Args:
            text: Single text string or list of text strings to classify
            
        Returns:
            Tuple containing:
            - List of predicted labels (0 for credible, 1 for misinformation)
            - List of prediction probabilities for each class
        """
        # Convert single string to list
        if isinstance(text, str):
            text = [text]
            
        # Get predictions from endpoint
        response = self.endpoint.predict(instances=text)
        
        # Extract predictions and probabilities
        predictions = response.predictions
        predicted_labels = [round(pred[0]) for pred in predictions]
        probabilities = [[1 - prob[0], prob[0]] for prob in predictions]
        
        return predicted_labels, probabilities
    
    def analyze_text(
        self, 
        text: str
    ) -> Dict[str, Union[int, List[float], Dict[str, Union[str, float]]]]:
        """Analyze a single text piece and return detailed results.
        
        Args:
            text (str): Text content to analyze
            
        Returns:
            Dictionary containing:
            - prediction: Predicted label (0 for credible, 1 for misinformation)
            - probabilities: List of prediction probabilities for each class
            - confidence_score: Overall confidence score
            - analysis: Detailed analysis including:
                - credibility_score: Score from 0-100
                - classification: Human-readable classification
                - confidence_level: Low/Medium/High based on probability
        """
        # Get raw prediction
        labels, probs = self.predict_text(text)
        prediction = labels[0]
        probabilities = probs[0]
        
        # Calculate confidence score (0-100)
        confidence_score = max(probabilities) * 100
        
        # Determine confidence level
        if confidence_score >= 90:
            confidence_level = "High"
        elif confidence_score >= 70:
            confidence_level = "Medium"
        else:
            confidence_level = "Low"
            
        # Calculate credibility score (inverse of misinformation probability)
        credibility_score = (1 - probabilities[1]) * 100
        
        # Determine classification
        if prediction == 0:
            classification = "Likely Credible"
        else:
            classification = "Potential Misinformation"
            
        # Compile detailed analysis
        analysis = {
            "credibility_score": round(credibility_score, 2),
            "classification": classification,
            "confidence_level": confidence_level,
            "prediction_confidence": round(confidence_score, 2)
        }
        
        return {
            "prediction": prediction,
            "probabilities": probabilities,
            "confidence_score": round(confidence_score, 2),
            "analysis": analysis
        }
        
    def batch_analyze_texts(
        self,
        texts: List[str]
    ) -> List[Dict[str, Union[int, List[float], Dict[str, Union[str, float]]]]]:
        """Analyze multiple texts in batch.
        
        Args:
            texts (List[str]): List of text contents to analyze
            
        Returns:
            List of analysis results for each text
        """
        labels, probs = self.predict_text(texts)
        return [
            self.analyze_text(text) 
            for text, label, prob in zip(texts, labels, probs)
        ]

def initialize_prediction_service(
    project_id: str,
    endpoint_id: str,
    location: str = "us-central1"
) -> PredictionService:
    """Initialize and return a PredictionService instance.
    
    Args:
        project_id (str): Google Cloud project ID
        endpoint_id (str): Vertex AI endpoint ID
        location (str): Google Cloud region
        
    Returns:
        PredictionService: Initialized prediction service instance
    """
    return PredictionService(project_id, endpoint_id, location)

if __name__ == "__main__":
    # Example usage
    project_id = "your-project-id"
    endpoint_id = "your-endpoint-id"
    
    # Initialize prediction service
    prediction_service = initialize_prediction_service(project_id, endpoint_id)
    
    # Example single text analysis
    text = "Sample article text to analyze"
    result = prediction_service.analyze_text(text)
    print("Analysis result:")
    print(json.dumps(result, indent=2))
    
    # Example batch analysis
    texts = [
        "First article text to analyze",
        "Second article text to analyze"
    ]
    results = prediction_service.batch_analyze_texts(texts)
    print("\nBatch analysis results:")
    print(json.dumps(results, indent=2))