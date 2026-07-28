from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.routes import health

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(
    health.router,
    prefix=settings.api_v1_prefix,
    tags=["health"],
)