import os
import json
from pathlib import Path
from typing import Optional, Dict

CONFIG_DIR = Path.home() / ".config" / "ghl"
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_config_from_file() -> Dict[str, str]:
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def get_config(api_key: Optional[str] = None, location_id: Optional[str] = None) -> Dict[str, Optional[str]]:
    file_config = get_config_from_file()

    # Priority: args > env > file
    final_api_key = api_key or os.environ.get("GHL_API_KEY") or file_config.get("api_key")
    final_location_id = location_id or os.environ.get("GHL_LOCATION_ID") or file_config.get("location_id")

    return {
        "api_key": final_api_key,
        "location_id": final_location_id
    }
