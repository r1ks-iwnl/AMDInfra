from jose import jwt
from datetime import datetime, timedelta, UTC

from ..config import get_settings

settings = get_settings()

def create_access_token(sub: str) -> str:
    payload = {"sub": sub, "exp": datetime.now(UTC) + timedelta(hours=8)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms="HS256")
    return payload["sub"]
