from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    return {"username": payload["sub"], "role": payload["role"]}


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")

    return current_user
