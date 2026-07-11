from jose import JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

from ..config import get_settings
from . import jwt as jwt_utils

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

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        return jwt_utils.decode_access_token(token)
    except JWTError:
        raise HTTPException(401, "Token invalid or expired.")
