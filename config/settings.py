"""Configuration settings for OCR to PDF converter."""

import json
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG = {
    "ocr_config": {
        "lang": "eng",
        "confidence_threshold": 70,
    },
    "pdf_config": {
        "compression": True,
        "output_quality": "high"
    }
}

def get_config() -> Dict[str, Any]:
    """Get configuration settings."""
    config_path = Path(__file__).parent / "config.json"
    
    if not config_path.exists():
        # Create default config if it doesn't exist
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
        
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration settings."""
    try:
        config_path = Path(__file__).parent / "config.json"
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception:
        return False
