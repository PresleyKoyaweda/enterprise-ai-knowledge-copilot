from fastapi import APIRouter, HTTPException

from app.models.auth import LoginRequest, TokenResponse
from app.db.fake_users import get_user
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    user = get_user(request.username)

    if user is None or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_access_token(subject=user["username"], role=user["role"])

    return TokenResponse(access_token=token)