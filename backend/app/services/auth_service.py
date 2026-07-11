import httpx
from jose import jwt

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

    try:
        id_token = resp.json().get("id_token", "")
        email = jwt.get_unverified_claims(id_token).get("email")
        if not email: raise ValueError()
    except Exception:
        raise ValueError("Invalid or missing Google ID Token.")

    return authorize_and_generate_token(email)

def authorize_and_generate_token(email: str) -> str:

    if not any(email.endswith(domain) for domain in settings.allowed_domains_list):
        raise PermissionError(f"Access denied: Email domain {email} isn't authorized.")
    
    return create_access_token(sub=email)
