"""
Training module for the misinformation detection model using Google Cloud Vertex AI.
"""
import os
from typing import Dict, List, Optional
import pandas as pd
from google.cloud import aiplatform
from google.cloud import storage

class ModelTrainer:
    def __init__(self, project_id: str, location: str = "us-central1", bucket_name: str = None):
        """Initialize the model trainer."""
        self.project_id = project_id
        self.location = location
        self.bucket_name = bucket_name or f"{project_id}-ml-data"
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        # Initialize storage client
        self.storage_client = storage.Client()
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Create storage bucket if it doesn't exist."""
        try:
            self.bucket = self.storage_client.get_bucket(self.bucket_name)
        except:
            self.bucket = self.storage_client.create_bucket(self.bucket_name)

    def prepare_training_data(self, data: List[Dict], output_file: str = "training_data.csv"):
        """
        Prepare and upload training data to Google Cloud Storage.
        
        Args:
            data: List of dictionaries containing:
                - claim: The text claim
                - label: TRUE/FALSE/UNCLEAR
                - source: Source of the claim
                - verification_date: When it was fact-checked
        """
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Add any necessary preprocessing here
        # For example, cleaning text, encoding labels, etc.
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        # Upload to GCS
        blob = self.bucket.blob(f"training_data/{output_file}")
        blob.upload_from_filename(output_file)
        
        return f"gs://{self.bucket_name}/training_data/{output_file}"

    def train_model(self, 
                   training_data_path: str,
                   model_display_name: str = "misinformation-detector",
                   training_fraction: float = 0.8,
                   validation_fraction: float = 0.1) -> aiplatform.Model:
        """
        Train a custom model for misinformation detection.
        
        Args:
            training_data_path: GCS path to training data
            model_display_name: Name for the model
            training_fraction: Fraction of data to use for training
            validation_fraction: Fraction of data to use for validation
        """
        # Create a dataset in Vertex AI
        dataset = aiplatform.TextDataset.create(
            display_name=f"{model_display_name}-dataset",
            gcs_source=training_data_path,
            import_schema_uri=aiplatform.schema.dataset.ioformat.text.multi_label_classification
        )

        # Configure the training job
        training_job = aiplatform.AutoMLTextTrainingJob(
            display_name=model_display_name,
            prediction_type="classification"
        )

        # Start training
        model = training_job.run(
            dataset=dataset,
            training_fraction_split=training_fraction,
            validation_fraction_split=validation_fraction,
            test_fraction_split=1 - training_fraction - validation_fraction,
            budget_milli_node_hours=8000,  # Adjust based on needs
            model_display_name=model_display_name
        )

        return model

    def deploy_model(self, model: aiplatform.Model) -> aiplatform.Endpoint:
        """
        Deploy the trained model to an endpoint.
        
        Args:
            model: Trained Vertex AI model
        """
        endpoint = model.deploy(
            machine_type="n1-standard-2",
            min_replica_count=1,
            max_replica_count=2,
            accelerator_type=None,
            accelerator_count=None
        )
        
        return endpoint

    def evaluate_model(self, model: aiplatform.Model, test_data: List[Dict]) -> Dict:
        """
        Evaluate model performance on test data.
        
        Args:
            model: Trained model
            test_data: List of test cases
        """
        # Get predictions for test data
        endpoint = model.get_endpoint()
        predictions = endpoint.predict([item["claim"] for item in test_data])
        
        # Calculate metrics
        metrics = model.get_model_evaluation().metrics
        
        return {
            "accuracy": metrics.get("accuracy"),
            "precision": metrics.get("precision"),
            "recall": metrics.get("recall"),
            "f1_score": metrics.get("f1_score"),
            "confusion_matrix": metrics.get("confusion_matrix"),
            "model_version": model.version_id,
            "training_date": model.create_time
        }