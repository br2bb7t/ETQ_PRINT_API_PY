from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from api.response.api_response import ApiResponse
from infrastructure.database.db_context import get_db_session
from infrastructure.logging.LoggerImplements import LoggerImplements

health_router = APIRouter(prefix="/health", tags=["Health"])

logger = LoggerImplements("HealthController")


@health_router.get("", summary="Health Check", description="Checks SQLite connection", response_model=ApiResponse)
async def health_check():

    method = "health_check"
    logger.log_information("Starting full health check...", method)

    try:

        with get_db_session() as session:
            session.execute(text("SELECT 1"))

        return ApiResponse.create_successful(
            result="Database connection successful",
            meta=None,
            messages=None,
        )

    except Exception as ex:

        logger.log_error(f"Health check failed: {str(ex)}", method)

        error_response = ApiResponse.create_error("Database connection failed")

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=error_response.model_dump(by_alias=True),
        )
