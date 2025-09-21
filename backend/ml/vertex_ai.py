from google.cloud import aiplatform
from google.cloud import storage
import os
import tempfile
import joblib

class VertexAIManager:
    def __init__(self, project_id, location="us-central1"):
        """Initialize the Vertex AI manager.
        
        Args:
            project_id (str): Google Cloud project ID
            location (str): Google Cloud region for Vertex AI resources
        """
        self.project_id = project_id
        self.location = location
        aiplatform.init(project=project_id, location=location)
        
    def deploy_model(self, model_dir, model_name, machine_type="n1-standard-2"):
        """Deploy a scikit-learn model to Vertex AI.
        
        Args:
            model_dir (str): GCS directory containing the model files
            model_name (str): Name for the deployed model
            machine_type (str): Machine type for model deployment
            
        Returns:
            Model: Deployed model instance
        """
        # Create model resource in Vertex AI
        model = aiplatform.Model.upload(
            display_name=model_name,
            artifact_uri=model_dir,
            serving_container_image_uri=(
                "us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest"
            ),
            instance_schema_uri=f"gs://google-cloud-aiplatform/schema/predict/instance/text_1.0.0.yaml",
            parameters_schema_uri=f"gs://google-cloud-aiplatform/schema/predict/params/text_1.0.0.yaml",
            serving_container_predict_route="/predict",
            serving_container_health_route="/health",
        )
        
        # Deploy the model
        endpoint = model.deploy(
            machine_type=machine_type,
            min_replica_count=1,
            max_replica_count=1,
            sync=True
        )
        
        print(f"Model {model_name} deployed successfully")
        return model, endpoint
    
    def get_prediction(self, endpoint, instances):
        """Get predictions from a deployed model.
        
        Args:
            endpoint: Vertex AI endpoint
            instances (list): List of text instances to get predictions for
            
        Returns:
            list: Predictions for the provided instances
        """
        predictions = endpoint.predict(instances=instances)
        return predictions
    
    def create_batch_prediction_job(
        self,
        model,
        source_uri,
        destination_uri,
        machine_type="n1-standard-2"
    ):
        """Create a batch prediction job.
        
        Args:
            model: Vertex AI model
            source_uri (str): GCS URI containing the input data
            destination_uri (str): GCS URI for prediction output
            machine_type (str): Machine type for the batch job
            
        Returns:
            BatchPredictionJob: Created batch prediction job
        """
        batch_prediction_job = model.batch_predict(
            source_uri=source_uri,
            destination_uri=destination_uri,
            machine_type=machine_type,
            sync=True
        )
        
        print(f"Batch prediction job completed. Results at: {destination_uri}")
        return batch_prediction_job
    
    def list_endpoints(self):
        """List all model endpoints in the project.
        
        Returns:
            list: List of model endpoints
        """
        endpoints = aiplatform.Endpoint.list()
        return endpoints
    
    def get_endpoint(self, endpoint_name):
        """Get a specific endpoint by name.
        
        Args:
            endpoint_name (str): Name of the endpoint to retrieve
            
        Returns:
            Endpoint: Retrieved endpoint instance
        """
        endpoint = aiplatform.Endpoint.get(endpoint_name=endpoint_name)
        return endpoint
        
    def delete_endpoint(self, endpoint):
        """Delete a model endpoint.
        
        Args:
            endpoint: Endpoint to delete
        """
        endpoint.delete(sync=True)
        print(f"Endpoint deleted successfully")
        
    def undeploy_model(self, model, endpoint):
        """Undeploy a model and delete its endpoint.
        
        Args:
            model: Model to undeploy
            endpoint: Endpoint to delete
        """
        self.delete_endpoint(endpoint)
        model.delete(sync=True)
        print(f"Model undeployed and deleted successfully")

def initialize_vertex_ai(project_id, location="us-central1"):
    """Initialize and return a VertexAIManager instance.
    
    Args:
        project_id (str): Google Cloud project ID
        location (str): Google Cloud region for Vertex AI resources
        
    Returns:
        VertexAIManager: Initialized Vertex AI manager instance
    """
    return VertexAIManager(project_id, location)

if __name__ == "__main__":
    # Example usage
    project_id = "your-project-id"
    model_name = "misinformation-detector"
    model_dir = "gs://your-model-bucket/models/misinformation_detector"
    
    # Initialize Vertex AI manager
    vertex_manager = initialize_vertex_ai(project_id)
    
    # Deploy model
    model, endpoint = vertex_manager.deploy_model(model_dir, model_name)
    
    # Make predictions
    sample_texts = ["Sample article text to classify"]
    predictions = vertex_manager.get_prediction(endpoint, sample_texts)
    print(f"Predictions: {predictions}")
    
    # Clean up (optional)
    vertex_manager.undeploy_model(model, endpoint)