from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.auth import TokenResponse
from app.db.fake_users import get_user
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    user = get_user(form_data.username)

    if user is None or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_access_token(subject=user["username"], role=user["role"])

    return TokenResponse(access_token=token)