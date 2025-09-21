# Stub file to replace problematic Google Cloud ML prediction service
# This allows the app to run without Google Cloud dependencies

def get_prediction_service():
    """Return None since Google Cloud ML prediction is not available."""
    return None

class PredictionService:
    """Stub prediction service that doesn't require Google Cloud."""
    
    def __init__(self, project_id=None, endpoint_id=None, location=None):
        self.available = False
    
    def analyze_text(self, text):
        """Stub method - returns None since service not available."""
        return None
    
    def predict(self, instances):
        """Stub method - returns empty predictions."""
        return []