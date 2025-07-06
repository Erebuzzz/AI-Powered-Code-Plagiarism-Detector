"""
JSON serialization utilities for handling numpy and other non-serializable types
"""
import json
import numpy as np
from decimal import Decimal

class NumpyJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles numpy types and other common non-serializable objects"""
    
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif hasattr(obj, 'item'):  # numpy scalar
            return obj.item()
        return super().default(obj)

def safe_json_serialize(data):
    """Safely serialize data to JSON, handling numpy types"""
    return json.loads(json.dumps(data, cls=NumpyJSONEncoder))

def convert_numpy_types(obj):
    """Recursively convert numpy types in nested structures"""
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'item'):  # numpy scalar
        return obj.item()
    return obj
