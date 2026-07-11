import httpx
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests

from ..auth.jwt import create_access_token
from ..config import get_settings

settings = get_settings()

async def authenticate_with_google(code: str, redirect_uri: str, code_verifier: str | None = None) -> str:
    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier

    async with httpx.AsyncClient() as client:
        resp = await client.post("https://oauth2.googleapis.com/token", data=payload)
        
    if resp.status_code != 200:
        raise ValueError("Google token exchange failed.")

    raw_id_token = resp.json().get("id_token", "")

    try:
        id_info = id_token.verify_oauth2_token(
            raw_id_token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        email = id_info.get("email")
        if not email: raise ValueError()
    except Exception:
        raise ValueError("Invalid Google ID Token signature or claims.")

    return authorize_and_generate_token(email)

def authorize_and_generate_token(email: str) -> str:

    if not any(email.endswith(domain) for domain in settings.allowed_domains_list):
        raise PermissionError(f"Access denied: Email domain {email} isn't authorized.")
    
    return create_access_token(sub=email)
