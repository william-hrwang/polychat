import json
import os

def load_config(service_name):
    """
    Load configuration for a specific service from the config file.
    
    Args:
        service_name (str): Name of the service (translation, chat, auth, tts)
        
    Returns:
        dict: Configuration for the specified service
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'backend_config.json')
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config['services'][service_name]
    except FileNotFoundError:
        print(f"⚠️ Configuration file not found at {config_path}")
        return None
    except KeyError:
        print(f"⚠️ Configuration for service '{service_name}' not found")
        return None
    except json.JSONDecodeError:
        print(f"⚠️ Invalid JSON in configuration file {config_path}")
        return None 