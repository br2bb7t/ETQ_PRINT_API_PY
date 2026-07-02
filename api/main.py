from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.controllers.health_controller import health_router
from api.controllers.label_controller import label_router
from api.response.api_response import ApiResponse
from api.routes.docs_routes import router as docs_router
from application.constants import constants
from application.constants.constants import APP_TITLE, APP_VERSION
from application.services.database_initializer import DatabaseInitializer
from application.services.seed_data_initializer import SeedDataInitializer
from config.config import Config


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    DatabaseInitializer.initialize()
    SeedDataInitializer.seed()

    yield


def create_app() -> FastAPI:
    Config()

    app = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(docs_router)
    app.include_router(health_router)
    app.include_router(label_router)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            api_response = ApiResponse.create_error(constants.ERR_NOT_FOUND, meta=None)
            return JSONResponse(
                status_code=404,
                content=api_response.model_dump(by_alias=True),
            )
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    return app


app = create_app()
