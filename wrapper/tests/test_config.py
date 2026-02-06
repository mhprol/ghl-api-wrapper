import os
import json
import yaml
import pytest
from unittest.mock import patch, mock_open, MagicMock
from ghl.config import get_config, load_profiles, get_profile, PROFILES_FILE, CONFIG_FILE

@pytest.fixture
def mock_profiles_yaml():
    return yaml.dump({
        'default': 'test_profile',
        'profiles': {
            'test_profile': {
                'api_key': 'profile_api_key',
                'location_id': 'profile_location_id'
            },
            'other_profile': {
                'api_key': 'other_api_key',
                'location_id': 'other_location_id'
            }
        }
    })

@pytest.fixture
def mock_config_json():
    return json.dumps({
        'api_key': 'file_api_key',
        'location_id': 'file_location_id'
    })

def test_load_profiles_file_not_exists():
    with patch('ghl.config.PROFILES_FILE') as mock_path:
        mock_path.exists.return_value = False
        profiles = load_profiles()
        assert profiles == {'default': None, 'profiles': {}}

def test_load_profiles_success(mock_profiles_yaml):
    with patch('ghl.config.PROFILES_FILE') as mock_path, \
         patch('builtins.open', mock_open(read_data=mock_profiles_yaml)):
        mock_path.exists.return_value = True
        profiles = load_profiles()
        assert profiles['default'] == 'test_profile'
        assert 'test_profile' in profiles['profiles']

def test_get_profile_default(mock_profiles_yaml):
    with patch('ghl.config.PROFILES_FILE') as mock_path, \
         patch('builtins.open', mock_open(read_data=mock_profiles_yaml)):
        mock_path.exists.return_value = True
        profile = get_profile()
        assert profile['api_key'] == 'profile_api_key'

def test_get_profile_named(mock_profiles_yaml):
    with patch('ghl.config.PROFILES_FILE') as mock_path, \
         patch('builtins.open', mock_open(read_data=mock_profiles_yaml)):
        mock_path.exists.return_value = True
        profile = get_profile('other_profile')
        assert profile['api_key'] == 'other_api_key'

def test_config_priority_cli_args(mock_profiles_yaml, mock_config_json):
    # Priority 1: CLI Args
    with patch('ghl.config.PROFILES_FILE') as mock_profiles_path, \
         patch('ghl.config.CONFIG_FILE') as mock_config_path, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch.dict(os.environ, {'GHL_API_KEY': 'env_api_key', 'GHL_LOCATION_ID': 'env_location_id'}):

        mock_profiles_path.exists.return_value = True
        mock_config_path.exists.return_value = True

        # We need to handle multiple open calls for different files
        # Since PROFILES_FILE and CONFIG_FILE are mocked objects, we check identity or name
        def side_effect(filename, *args, **kwargs):
            if filename == mock_profiles_path:
                return mock_open(read_data=mock_profiles_yaml)()
            elif filename == mock_config_path:
                return mock_open(read_data=mock_config_json)()
            return mock_open()()

        mocked_file.side_effect = side_effect

        config = get_config(api_key='arg_api_key', location_id='arg_location_id', profile_name='test_profile')

        assert config['api_key'] == 'arg_api_key'
        assert config['location_id'] == 'arg_location_id'

def test_config_priority_profile(mock_profiles_yaml, mock_config_json):
    # Priority 2: Profile
    with patch('ghl.config.PROFILES_FILE') as mock_profiles_path, \
         patch('ghl.config.CONFIG_FILE') as mock_config_path, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch.dict(os.environ, {'GHL_API_KEY': 'env_api_key', 'GHL_LOCATION_ID': 'env_location_id'}):

        mock_profiles_path.exists.return_value = True
        mock_config_path.exists.return_value = True

        def side_effect(filename, *args, **kwargs):
            if filename == mock_profiles_path:
                return mock_open(read_data=mock_profiles_yaml)()
            elif filename == mock_config_path:
                return mock_open(read_data=mock_config_json)()
            return mock_open()()

        mocked_file.side_effect = side_effect

        config = get_config(profile_name='test_profile')

        assert config['api_key'] == 'profile_api_key'
        assert config['location_id'] == 'profile_location_id'

def test_config_priority_env(mock_profiles_yaml, mock_config_json):
    # Priority 3: Env Vars (when no profile or profile missing keys)
    with patch('ghl.config.PROFILES_FILE') as mock_profiles_path, \
         patch('ghl.config.CONFIG_FILE') as mock_config_path, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch.dict(os.environ, {'GHL_API_KEY': 'env_api_key', 'GHL_LOCATION_ID': 'env_location_id'}):

        mock_profiles_path.exists.return_value = True
        mock_config_path.exists.return_value = True

        def side_effect(filename, *args, **kwargs):
            if filename == mock_profiles_path:
                # Profile that exists but has empty keys or different one
                 return mock_open(read_data=yaml.dump({'profiles': {'empty': {}}}))()
            elif filename == mock_config_path:
                return mock_open(read_data=mock_config_json)()
            return mock_open()()

        mocked_file.side_effect = side_effect

        config = get_config(profile_name='empty')

        assert config['api_key'] == 'env_api_key'
        assert config['location_id'] == 'env_location_id'

def test_config_priority_file(mock_profiles_yaml, mock_config_json):
    # Priority 4: Config File (when env vars missing)
    with patch('ghl.config.PROFILES_FILE') as mock_profiles_path, \
         patch('ghl.config.CONFIG_FILE') as mock_config_path, \
         patch('builtins.open', mock_open()) as mocked_file, \
         patch.dict(os.environ, {}, clear=True):

        mock_profiles_path.exists.return_value = True
        mock_config_path.exists.return_value = True

        def side_effect(filename, *args, **kwargs):
            if filename == mock_profiles_path:
                 return mock_open(read_data=yaml.dump({'profiles': {'empty': {}}}))()
            elif filename == mock_config_path:
                return mock_open(read_data=mock_config_json)()
            return mock_open()()

        mocked_file.side_effect = side_effect

        config = get_config(profile_name='empty')

        assert config['api_key'] == 'file_api_key'
        assert config['location_id'] == 'file_location_id'
