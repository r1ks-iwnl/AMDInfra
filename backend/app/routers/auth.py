from fastapi import APIRouter, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request

from ..services.auth_service import authenticate_with_google
from ..config import get_settings

settings = get_settings()
router = APIRouter(tags=["Auth"])

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope" : "openid email profile"}
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", include_in_schema=False)
@router.post("/callback", name="callback_post", summary="Processes Swagger's OAuth login")
async def callback(request: Request):
    is_post = request.method == "POST"
    data = await request.form() if is_post else request.query_params
    
    if not (code := data.get("code")):
        raise HTTPException(status_code=400, detail="Authorization code missing.")

    redirect_uri = data.get("redirect_uri") or (
        "http://localhost:8000/docs/oauth2-redirect" if is_post else str(request.url_for("callback"))
    )

    try:
        jwt_token = await authenticate_with_google(
            code=code, 
            redirect_uri=redirect_uri, 
            code_verifier=data.get("code_verifier")
        )
        return {"access_token": jwt_token, "token_type": "bearer"}
        
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
