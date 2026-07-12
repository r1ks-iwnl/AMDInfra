from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.requests import Request
import urllib.parse

from ..services.auth_service import authenticate_with_google
from ..config import get_settings

settings = get_settings()
router = APIRouter(tags=["Auth"])

@router.get("/login")
async def login(request: Request):
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": str(request.url_for("callback")),
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }

    google_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return RedirectResponse(google_url)

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
    # 1. Dacă cererea e POST, vine de la Swagger UI -> Întoarcem JSON pur
        if is_post:
            return {"access_token": jwt_token, "token_type": "bearer"}
            
        # 2. Dacă e GET, vine din fluxul normal de browser (Frontend pop-up) -> Întoarcem scriptul HTML
        html_script = f"""
        <script>
            window.opener.postMessage({{ token: "{jwt_token}" }}, "http://localhost:5173");
        </script>
        """
        return HTMLResponse(content=html_script)
        
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
