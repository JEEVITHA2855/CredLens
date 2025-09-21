from google.cloud import storage
import os
import tempfile

class CloudStorageManager:
    def __init__(self, project_id, bucket_name):
        """Initialize the Cloud Storage manager.
        
        Args:
            project_id (str): Google Cloud project ID
            bucket_name (str): Name of the Cloud Storage bucket
        """
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.storage_client = storage.Client(project=project_id)
        self.bucket = self.storage_client.bucket(bucket_name)
        
    def ensure_bucket_exists(self):
        """Ensure the specified bucket exists, create if it doesn't."""
        if not self.bucket.exists():
            self.bucket = self.storage_client.create_bucket(
                self.bucket_name, 
                location="us-central1"
            )
            print(f"Created bucket: {self.bucket_name}")
    
    def upload_file(self, source_path, destination_blob_path):
        """Upload a file to Cloud Storage.
        
        Args:
            source_path (str): Local path to the file to upload
            destination_blob_path (str): Path in the bucket where the file will be stored
        """
        blob = self.bucket.blob(destination_blob_path)
        blob.upload_from_filename(source_path)
        print(f"Uploaded {source_path} to {destination_blob_path}")
        
    def download_file(self, source_blob_path, destination_path):
        """Download a file from Cloud Storage.
        
        Args:
            source_blob_path (str): Path to the file in the bucket
            destination_path (str): Local path where the file will be downloaded
        """
        blob = self.bucket.blob(source_blob_path)
        blob.download_to_filename(destination_path)
        print(f"Downloaded {source_blob_path} to {destination_path}")
        
    def upload_directory(self, source_dir, destination_prefix=""):
        """Upload an entire directory to Cloud Storage.
        
        Args:
            source_dir (str): Local directory path to upload
            destination_prefix (str): Prefix to add to the blob paths
        """
        for root, _, files in os.walk(source_dir):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, source_dir)
                blob_path = os.path.join(destination_prefix, relative_path)
                self.upload_file(local_path, blob_path)
                
    def download_directory(self, source_prefix, destination_dir):
        """Download all files with a given prefix from Cloud Storage.
        
        Args:
            source_prefix (str): Prefix to filter blobs in the bucket
            destination_dir (str): Local directory where files will be downloaded
        """
        os.makedirs(destination_dir, exist_ok=True)
        blobs = self.bucket.list_blobs(prefix=source_prefix)
        
        for blob in blobs:
            if not blob.name.endswith('/'):  # Skip directories
                relative_path = os.path.relpath(blob.name, source_prefix)
                local_path = os.path.join(destination_dir, relative_path)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                self.download_file(blob.name, local_path)
                
    def list_files(self, prefix=""):
        """List all files in the bucket with a given prefix.
        
        Args:
            prefix (str): Optional prefix to filter results
            
        Returns:
            list: List of blob names in the bucket
        """
        return [blob.name for blob in self.bucket.list_blobs(prefix=prefix)]
    
    def delete_file(self, blob_path):
        """Delete a file from Cloud Storage.
        
        Args:
            blob_path (str): Path to the file in the bucket to delete
        """
        blob = self.bucket.blob(blob_path)
        blob.delete()
        print(f"Deleted {blob_path}")
        
    def get_signed_url(self, blob_path, expiration=3600):
        """Generate a signed URL for temporary access to a file.
        
        Args:
            blob_path (str): Path to the file in the bucket
            expiration (int): URL expiration time in seconds (default: 1 hour)
            
        Returns:
            str: Signed URL for accessing the file
        """
        blob = self.bucket.blob(blob_path)
        url = blob.generate_signed_url(
            version="v4",
            expiration=expiration,
            method="GET"
        )
        return url

def initialize_storage(project_id, bucket_name):
    """Initialize and return a CloudStorageManager instance.
    
    Args:
        project_id (str): Google Cloud project ID
        bucket_name (str): Name of the Cloud Storage bucket
        
    Returns:
        CloudStorageManager: Initialized storage manager instance
    """
    storage_manager = CloudStorageManager(project_id, bucket_name)
    storage_manager.ensure_bucket_exists()
    return storage_manager

if __name__ == "__main__":
    # Example usage
    project_id = "your-project-id"
    bucket_name = "your-model-bucket"
    
    # Initialize storage manager
    storage_manager = initialize_storage(project_id, bucket_name)
    
    # Example operations
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Test content")
        temp_path = temp_file.name
    
    # Upload file
    storage_manager.upload_file(temp_path, "test/example.txt")
    
    # List files
    files = storage_manager.list_files()
    print("Files in bucket:", files)
    
    # Get signed URL
    url = storage_manager.get_signed_url("test/example.txt")
    print("Signed URL:", url)
    
    # Clean up
    storage_manager.delete_file("test/example.txt")
    os.unlink(temp_path)