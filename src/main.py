import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.openapi.utils import get_openapi
import redis.asyncio as redis

from src.auth.views import router as auth_router
from src.tracking.views import router as tracking_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    app.state.redis = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        decode_responses=True,
    )

    await app.state.redis.ping()

    yield  # приложение работает здесь

    # SHUTDOWN
    await app.state.redis.aclose()

app = FastAPI(lifespan=lifespan)



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="BUS-TRACKER API",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    openapi_schema["security"] = [{"HTTPBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(auth_router)
app.include_router(tracking_router)










