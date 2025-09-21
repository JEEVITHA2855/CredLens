"""
Train and deploy a misinformation detection model using scikit-learn and Google Cloud Vertex AI.
"""
import os
import json
import pandas as pd
import numpy as np
from google.cloud import aiplatform
from google.cloud import storage
from typing import Dict, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from datetime import datetime

class MisinformationModel:
    def __init__(self, 
                project_id: str,
                location: str = "us-central1",
                bucket_name: Optional[str] = None):
        """Initialize the model trainer."""
        self.project_id = project_id
        self.location = location
        self.bucket_name = bucket_name or f"{project_id}-ml-data"
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        # Initialize storage client
        self.storage_client = storage.Client()
        self.bucket = self._ensure_bucket_exists()
        
        # Initialize model parameters
        self.bert_preprocess = None
        self.bert_encoder = None
        self.model = None

    def _ensure_bucket_exists(self):
        """Create or get the GCS bucket."""
        try:
            return self.storage_client.get_bucket(self.bucket_name)
        except:
            return self.storage_client.create_bucket(self.bucket_name)

    def train_model(self, train_data: pd.DataFrame, val_data: pd.DataFrame):
        """Train the model using the provided data."""
        print("Training model...")
        
        # Train the pipeline
        self.model.fit(train_data['cleaned_claim'], train_data['label'])
        
        # Evaluate on validation data
        val_pred = self.model.predict(val_data['cleaned_claim'])
        val_metrics = {
            'classification_report': classification_report(val_data['label'], val_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(val_data['label'], val_pred).tolist()
        }
        
        return val_metrics

    def evaluate_model(self, test_data: pd.DataFrame):
        """Evaluate the model on test data."""
        print("\nEvaluating model...")
        
        test_pred = self.model.predict(test_data['cleaned_claim'])
        metrics = {
            'classification_report': classification_report(test_data['label'], test_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(test_data['label'], test_pred).tolist()
        }
        
        return metrics

    def save_model_to_gcs(self, model_name: str):
        """Save the trained model to Google Cloud Storage."""
        local_path = f"models/{model_name}"
        gcs_path = f"gs://{self.bucket_name}/models/{model_name}"
        
        # Save local copy
        self.model.save(local_path)
        
        # Upload to GCS
        for root, _, files in os.walk(local_path):
            for file in files:
                local_file = os.path.join(root, file)
                gcs_file = os.path.join(
                    gcs_path,
                    os.path.relpath(local_file, local_path)
                )
                blob = self.bucket.blob(gcs_file.replace("gs://", "").split("/", 1)[1])
                blob.upload_from_filename(local_file)
        
        return gcs_path

    def deploy_model(self, 
                    model_name: str,
                    model_display_name: str = "misinformation-detector"):
        """Deploy the model to Vertex AI."""
        # Upload model artifacts
        gcs_path = self.save_model_to_gcs(model_name)
        
        # Create model in Vertex AI
        model = aiplatform.Model.upload(
            display_name=model_display_name,
            artifact_uri=gcs_path,
            serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-12:latest"
        )
        
        # Deploy model
        endpoint = model.deploy(
            machine_type="n1-standard-2",
            min_replica_count=1,
            max_replica_count=2
        )
        
        return endpoint

def main():
    # Load environment variables
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Initialize model trainer
    trainer = MisinformationModel(project_id, location)
    
    # Load processed data
    train_data = pd.read_csv("processed_data/train.csv")
    val_data = pd.read_csv("processed_data/validation.csv")
    test_data = pd.read_csv("processed_data/test.csv")
    
    # Train model
    history = trainer.train_model(train_data, val_data)
    
    # Evaluate model
    metrics = trainer.evaluate_model(test_data)
    print("\nTest metrics:", metrics)
    
    # Save training metrics
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = f"misinformation_detector_{timestamp}"
    
    metrics_data = {
        "model_name": model_name,
        "history": history.history,
        "test_metrics": metrics,
        "timestamp": timestamp
    }
    
    with open(f"processed_data/metrics_{timestamp}.json", "w") as f:
        json.dump(metrics_data, f, indent=2)
    
    # Deploy model
    endpoint = trainer.deploy_model(model_name)
    print(f"\nModel deployed to endpoint: {endpoint.resource_name}")

if __name__ == "__main__":
    main()