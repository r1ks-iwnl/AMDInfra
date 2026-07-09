from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

from ..config import get_settings

settings = get_settings()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
    tokenUrl="/auth/callback",
    scopes={
        "openid": "OpenID Connect",
        "email": "Email address access",
        "profile": "User profile access"
    }
)

def create_access_token(sub: str):
    payload = {"sub": sub, "exp": datetime.now(UTC) + timedelta(hours=8)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(401, "Token invalid or expired.")
    
    return payload["sub"]
