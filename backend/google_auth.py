from google.oauth2 import id_token
from google.auth.transport import requests
import os
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google OAuth Client ID (set via environment variable or .env file)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

def verify_google_token(id_token_string: str) -> Optional[Dict]:
    """Verify Google ID token and return user info"""
    try:
        if not GOOGLE_CLIENT_ID:
            raise ValueError("GOOGLE_CLIENT_ID not configured")
        
        # Verify the ID token
        idinfo = id_token.verify_oauth2_token(
            id_token_string, 
            requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        
        # Verify the issuer
        if idinfo.get('iss') not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        
        return {
            'email': idinfo.get('email'),
            'name': idinfo.get('name'),
            'picture': idinfo.get('picture'),
            'sub': idinfo.get('sub')  # Google user ID
        }
    except ValueError as e:
        print(f"Google token verification error: {e}")
        return None
    except Exception as e:
        print(f"Error verifying Google token: {e}")
        import traceback
        traceback.print_exc()
        return None

