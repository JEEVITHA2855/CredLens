import os
import json
from google.cloud import storage
from google.cloud import aiplatform
from google.oauth2 import service_account

class EnvironmentSetup:
    def __init__(self, credentials_path: str):
        """Initialize environment setup.
        
        Args:
            credentials_path (str): Path to the Google Cloud service account key file
        """
        self.credentials_path = os.path.abspath(credentials_path)
        
    def validate_credentials(self) -> bool:
        """Validate Google Cloud credentials.
        
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        try:
            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            
            # Test with storage client
            storage_client = storage.Client(credentials=credentials)
            storage_client.list_buckets(max_results=1)
            
            return True
        except Exception as e:
            print(f"Credential validation failed: {str(e)}")
            return False
            
    def setup_environment(
        self,
        project_id: str,
        bucket_name: str,
        location: str = "us-central1"
    ) -> bool:
        """Set up the Google Cloud environment.
        
        Args:
            project_id (str): Google Cloud project ID
            bucket_name (str): Name for the Cloud Storage bucket
            location (str): Google Cloud region
            
        Returns:
            bool: True if setup is successful, False otherwise
        """
        try:
            # Set environment variables
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
            os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
            os.environ["GOOGLE_CLOUD_LOCATION"] = location
            os.environ["GOOGLE_CLOUD_BUCKET"] = bucket_name
            
            # Initialize clients
            storage_client = storage.Client()
            
            # Ensure bucket exists
            bucket = storage_client.bucket(bucket_name)
            if not bucket.exists():
                bucket = storage_client.create_bucket(bucket_name, location=location)
                print(f"Created bucket: {bucket_name}")
            
            # Initialize Vertex AI
            aiplatform.init(
                project=project_id,
                location=location,
                staging_bucket=bucket_name
            )
            
            print("Environment setup completed successfully")
            return True
            
        except Exception as e:
            print(f"Environment setup failed: {str(e)}")
            return False
            
    def save_config(self, config_path: str) -> None:
        """Save the current configuration to a file.
        
        Args:
            config_path (str): Path to save the configuration file
        """
        config = {
            "credentials_path": self.credentials_path,
            "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
            "location": os.getenv("GOOGLE_CLOUD_LOCATION"),
            "bucket_name": os.getenv("GOOGLE_CLOUD_BUCKET")
        }
        
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
            
        print(f"Configuration saved to: {config_path}")
            
    @classmethod
    def load_config(cls, config_path: str) -> "EnvironmentSetup":
        """Load configuration from a file and create an EnvironmentSetup instance.
        
        Args:
            config_path (str): Path to the configuration file
            
        Returns:
            EnvironmentSetup: Initialized environment setup instance
        """
        with open(config_path, "r") as f:
            config = json.load(f)
            
        setup = cls(config["credentials_path"])
        setup.setup_environment(
            config["project_id"],
            config["bucket_name"],
            config["location"]
        )
        
        return setup

def check_environment():
    """Check if the required environment variables are set.
    
    Returns:
        bool: True if all required variables are set, False otherwise
    """
    required_vars = [
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION",
        "GOOGLE_CLOUD_BUCKET"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        return False
        
    return True

if __name__ == "__main__":
    # Example usage
    credentials_path = "path/to/your/service-account-key.json"
    project_id = "your-project-id"
    bucket_name = "your-model-bucket"
    config_path = "config/ml_config.json"
    
    # Create and validate setup
    setup = EnvironmentSetup(credentials_path)
    
    if setup.validate_credentials():
        # Perform setup
        if setup.setup_environment(project_id, bucket_name):
            # Save configuration
            setup.save_config(config_path)
            
            # Verify environment
            if check_environment():
                print("Environment is ready for ML operations")