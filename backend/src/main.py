import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .exceptions import HttpClientError, RemoteServiceError
from .api import settlement, merchant

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger("uvicorn.error")


# called at the start and end of the application
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting application... ")
    yield
    print("...shutting down application")


# start the app
app = FastAPI(lifespan=lifespan)
app.include_router(settlement.router)
app.include_router(merchant.router)


@app.exception_handler(HttpClientError)
async def http_client_error_handler(request: Request, exc: HttpClientError):
    return JSONResponse(
        # Client-side issue
        status_code=400,
        content={"error": exc.detail},
    )


@app.exception_handler(RemoteServiceError)
async def remote_service_error_handler(request: Request, exc: RemoteServiceError):
    return JSONResponse(
        # Bad Gateway (upstream issue)
        status_code=502,
        content={"error": exc.detail},
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ACME Payment API Middleware",
        version="0.1.0",
        description="The incredible ACME Payments API Middleware, empowering the tech from 1972.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
