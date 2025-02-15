from msal import ConfidentialClientApplication
import requests
import webbrowser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Microsoft Authentication credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/callback')
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPE = ['User.Read']

def get_auth_url():
    """
    Get Microsoft authentication URL
    Returns:
        Dictionary containing auth URL or error
    """
    try:
        app = ConfidentialClientApplication(
            client_id=CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=AUTHORITY
        )

        auth_url = app.get_authorization_request_url(
            scopes=SCOPE,
            redirect_uri=REDIRECT_URI,
            state=os.urandom(16).hex()  # For security
        )

        webbrowser.open(auth_url)

        return {
            "status": "success",
            "auth_url": auth_url
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to generate auth URL: {str(e)}"
        }

def handle_callback(code=None, error=None, error_description=None):
    """
    Handle Microsoft OAuth callback
    Args:
        code: Authorization code from Microsoft
        error: Error code if auth failed
        error_description: Detailed error message
    Returns:
        Dictionary containing token and user info or error
    """
    if error:
        return {
            "status": "error",
            "error": error,
            "error_description": error_description
        }

    if not code:
        return {
            "status": "error",
            "error": "No authorization code received"
        }

    try:
        # Initialize MSAL app
        app = ConfidentialClientApplication(
            client_id=CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=AUTHORITY
        )

        # Get token using authorization code
        result = app.acquire_token_by_authorization_code(
            code=code,
            scopes=SCOPE,
            redirect_uri=REDIRECT_URI
        )

        if "access_token" not in result:
            return {
                "status": "error",
                "error": "Failed to get access token",
                "details": result.get("error_description", "Unknown error")
            }

        # Get user details using the token
        user_details = get_user_details(result["access_token"])
        
        if user_details["status"] == "error":
            return user_details

        return {
            "status": "success",
            "access_token": result["access_token"],
            "user": user_details["user"]
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Token exchange failed: {str(e)}"
        }

def get_user_details(access_token):
    """
    Get user details from Microsoft Graph API
    Args:
        access_token: Valid Microsoft access token
    Returns:
        Dictionary containing user details or error
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(
            'https://graph.microsoft.com/v1.0/me',
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            user_data = response.json()
            return {
                "status": "success",
                "user": {
                    "id": user_data.get('id'),
                    "displayName": user_data.get('displayName'),
                    "givenName": user_data.get('givenName'),
                    "surname": user_data.get('surname'),
                    "userPrincipalName": user_data.get('userPrincipalName'),
                    "mail": user_data.get('mail'),
                    "jobTitle": user_data.get('jobTitle'),
                    "department": user_data.get('department'),
                    "officeLocation": user_data.get('officeLocation'),
                    "businessPhones": user_data.get('businessPhones', []),
                    "mobilePhone": user_data.get('mobilePhone')
                }
            }
        else:
            return {
                "status": "error",
                "error": f"Failed to get user details: {response.text}"
            }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": f"API request failed: {str(e)}"
        }