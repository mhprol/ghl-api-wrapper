import os
import json
import yaml
from pathlib import Path
from typing import Optional, Dict, Any

CONFIG_DIR = Path.home() / ".config" / "ghl"
CONFIG_FILE = CONFIG_DIR / "config.json"
PROFILES_FILE = CONFIG_DIR / "profiles.yaml"

def load_profiles() -> Dict[str, Any]:
    if not PROFILES_FILE.exists():
        return {'default': None, 'profiles': {}}
    try:
        with open(PROFILES_FILE) as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                return {'default': None, 'profiles': {}}
            return data
    except Exception:
        return {'default': None, 'profiles': {}}

def get_profile(name: str = None) -> Dict[str, str]:
    data = load_profiles()
    profile_name = name or data.get('default')
    if not profile_name:
        return {}
    return data.get('profiles', {}).get(profile_name, {})

def get_config_from_file() -> Dict[str, str]:
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {}
            return data
    except Exception:
        return {}

def get_config(api_key: Optional[str] = None, location_id: Optional[str] = None, profile_name: Optional[str] = None) -> Dict[str, Optional[str]]:
    file_config = get_config_from_file()
    profile_config = get_profile(profile_name)

    # Priority: args > profile > env > file
    final_api_key = api_key or profile_config.get("api_key") or os.environ.get("GHL_API_KEY") or file_config.get("api_key")
    final_location_id = location_id or profile_config.get("location_id") or os.environ.get("GHL_LOCATION_ID") or file_config.get("location_id")

    return {
        "api_key": final_api_key,
        "location_id": final_location_id
    }
