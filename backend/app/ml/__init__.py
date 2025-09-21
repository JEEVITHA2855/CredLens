"""ML package initialization"""
import os
import json
from typing import Dict, Optional

def load_ml_config() -> Optional[Dict]:
    """Load ML configuration from file"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'ml_config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading ML config: {e}")
        return None

ml_config = load_ml_config()