from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.routes import health, chat, documents, auth

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(
    health.router,
    prefix=settings.api_v1_prefix,
    tags=["health"],
)

app.include_router(
    chat.router,
    prefix=settings.api_v1_prefix,
    tags=["chat"],
)

app.include_router(
    documents.router,
    prefix=settings.api_v1_prefix,
    tags=["documents"],
)

app.include_router(
    auth.router, 
    prefix=settings.api_v1_prefix, 
    tags=["auth"],
    )