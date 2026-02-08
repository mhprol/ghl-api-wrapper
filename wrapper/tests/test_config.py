import os
import json
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from ghl.config import get_config, get_config_from_file, CONFIG_FILE

def test_get_config_from_file_no_file():
    with patch("pathlib.Path.exists", return_value=False):
        assert get_config_from_file() == {}

def test_get_config_from_file_exists():
    data = {"api_key": "file_key"}
    with patch("pathlib.Path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=json.dumps(data))):
            assert get_config_from_file() == data

def test_get_config_from_file_error():
    with patch("pathlib.Path.exists", return_value=True):
        with patch("builtins.open", side_effect=Exception("Read error")):
            assert get_config_from_file() == {}

def test_get_config_priority():
    # Args > Env > File

    # 1. Args only
    assert get_config(api_key="arg_key")["api_key"] == "arg_key"

    # 2. Env > File (Args None)
    with patch.dict(os.environ, {"GHL_API_KEY": "env_key"}):
        with patch("ghl.config.get_config_from_file", return_value={"api_key": "file_key"}):
            assert get_config()["api_key"] == "env_key"

    # 3. File only
    with patch.dict(os.environ, {}, clear=True):
        with patch("ghl.config.get_config_from_file", return_value={"api_key": "file_key"}):
            assert get_config()["api_key"] == "file_key"

    # 4. None
    with patch.dict(os.environ, {}, clear=True):
        with patch("ghl.config.get_config_from_file", return_value={}):
            assert get_config()["api_key"] is None
