"""
Authentication module for Schwab API
Handles loading credentials and initializing the API client
"""

import os
from schwab.auth import easy_client

def load_credentials():
    """
    Load API credentials from environment variables
    
    Returns:
        dict: Dictionary containing API credentials
    
    Raises:
        ValueError: If any required credentials are missing
    """
    # Required credentials for Schwab API authentication
    credentials = {
        'client_id': os.environ.get('SCHWAB_CLIENT_ID'),
        'client_secret': os.environ.get('SCHWAB_CLIENT_SECRET'),
        'redirect_uri': os.environ.get('SCHWAB_REDIRECT_URI'),
        'token_path': os.environ.get('SCHWAB_TOKEN_PATH', './token.json'),
    }
    
    # Check if all required credentials are available
    missing_creds = [k for k, v in credentials.items() if not v]
    if missing_creds:
        raise ValueError(f"Missing required credentials: {', '.join(missing_creds)}")
        
    return credentials

def initialize_client(credentials):
    """
    Initialize and authenticate with the Schwab API using easy_client
    
    Args:
        credentials (dict): API credentials dictionary
        
    Returns:
        schwab.client.Client: Authenticated API client
    """
    try:
        # Use the easy_client function with the correct parameter names
        client = easy_client(
            api_key=credentials['client_id'],
            app_secret=credentials['client_secret'],
            callback_url=credentials['redirect_uri'],
            token_path=credentials['token_path']
        )
        
        # Return authenticated client
        return client
    
    except Exception as e:
        print(f"Exception when authenticating with Schwab API: {e}")
        raise