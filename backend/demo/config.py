"""Configuration settings for the CredLens application."""
import os
from pathlib import Path
import json

def load_config_from_env():
    """Load configuration from environment variables."""
    return {
        'use_web_search': os.getenv('CREDLENS_USE_WEB_SEARCH', 'true').lower() == 'true',
        'use_fact_check_apis': os.getenv('CREDLENS_USE_FACT_CHECK_APIS', 'true').lower() == 'true',
        'debug_mode': os.getenv('CREDLENS_DEBUG', 'false').lower() == 'true'
    }

def load_config_from_dotenv():
    """Load configuration from .env file."""
    config = {
        'use_web_search': True,
        'use_fact_check_apis': True,
        'debug_mode': False
    }
    
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if '=' not in line:
                    continue
                key, value = line.strip().split('=', 1)
                if key == 'CREDLENS_USE_WEB_SEARCH':
                    config['use_web_search'] = value.lower() == 'true'
                elif key == 'CREDLENS_USE_FACT_CHECK_APIS':
                    config['use_fact_check_apis'] = value.lower() == 'true'
                elif key == 'CREDLENS_DEBUG':
                    config['debug_mode'] = value.lower() == 'true'
    return config

def setup_environment():
    """Setup environment variables and configuration."""
    # First try environment variables
    config = load_config_from_env()
    
    # If not complete, try .env file
    if not all(config.values()):
        env_config = load_config_from_dotenv()
        config.update(env_config)
    
    # Set environment variables
    os.environ['CREDLENS_USE_WEB_SEARCH'] = str(config['use_web_search']).lower()
    os.environ['CREDLENS_USE_FACT_CHECK_APIS'] = str(config['use_fact_check_apis']).lower()
    os.environ['CREDLENS_DEBUG'] = str(config['debug_mode']).lower()
    
    return True