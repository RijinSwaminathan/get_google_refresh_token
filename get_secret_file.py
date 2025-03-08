import google.auth
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Path to the JSON file of client secret
CLIENT_SECRETS_FILE = "/home/rijin/Downloads/client_secret_660170263543-mqb8hci3aj9gbqjdojq2t22tbh93nume.apps.googleusercontent.com.json"

# Path to store the refresh token
TOKEN_FILE = "/home/rijin/Downloads/ad_campaign_test/refresh_token.json"

# Scopes required for the Google Ads API
SCOPES = [
    "https://www.googleapis.com/auth/adwords" 
]

def get_credentials():
    """Gets the credentials for the Google Ads API."""
    
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as token_file:
                credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
                    info=json.load(token_file), scopes=SCOPES
                )

            if credentials.expired and credentials.refresh_token:
                request = google.auth.transport.requests.Request()
                credentials.refresh(request)
                with open(TOKEN_FILE, 'w') as token_file:
                    token_data = {
                        'token': credentials.token,
                        'refresh_token': credentials.refresh_token,
                        'token_uri': credentials.token_uri,
                        'client_id': credentials.client_id,
                        'client_secret': credentials.client_secret,
                        'scopes': credentials.scopes
                    }
                    json.dump(token_data, token_file)
                return credentials
        except Exception as e:
            logging.error(f"Error reading/refreshing token: {e}")
            if os.path.exists(TOKEN_FILE):
                os.remove(TOKEN_FILE)

    try:
        # verify the client secrets file exists
        if not os.path.exists(CLIENT_SECRETS_FILE):
            raise FileNotFoundError(f"Client secrets file not found at: {CLIENT_SECRETS_FILE}")
            
        # Load and validate client secrets
        with open(CLIENT_SECRETS_FILE, 'r') as f:
            client_config = json.load(f)
            logging.info("Client configuration loaded successfully")
            logging.debug(f"Available OAuth scopes: {SCOPES}")
            
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES
        )
        
        # select desktop applications for testing
        credentials = flow.run_local_server(
            port=0,  # Use any available port
            prompt='consent'
        )

        # Save the credentials
        with open(TOKEN_FILE, "w") as token_file:
            token_data = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            json.dump(token_data, token_file)
            logging.info(f"Credentials saved to {TOKEN_FILE}")
            
        return credentials
        
    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        raise
    
if __name__ == "__main__":
    try:
        credentials = get_credentials()
        print("\nAuthentication successful!")
        print(f"Token file saved to: {os.path.abspath(TOKEN_FILE)}")

        # use the credentials to access the Google Ads API
        
        print("Credentials obtained successfully!")
        print("Refresh token (stored in token.json):")
        # get the refresh token like this if needed (but it's already in the JSON file)
    except Exception as e:
        print(f"\nAuthentication failed: {e}")