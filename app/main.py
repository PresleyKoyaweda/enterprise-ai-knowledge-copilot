from fastapi import FastAPI

from app.api.v1.routes import auth, chat, documents, health
from app.core.config import settings

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
