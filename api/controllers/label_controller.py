from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.response.api_response import ApiResponse
from api.schemas.label_request import LabelRequest
from application.services.label_service import LabelService
from infrastructure.logging.LoggerImplements import LoggerImplements

label_router = APIRouter(
    prefix="/labels",
    tags=["Labels"],
)

label_service = LabelService()

logger = LoggerImplements("LabelController")


@label_router.post("/print", response_model=ApiResponse)
async def print_label(payload: LabelRequest):

    method = "print_label"

    logger.log_information(
        f"Request received. LPN={payload.request.lpn}",
        method,
    )

    try:

        response = label_service.print_label(
            lpn=payload.request.lpn,
        )

        if response.is_successful:

            logger.log_information(
                f"Process completed successfully. LPN={payload.request.lpn}",
                method,
            )

        else:

            logger.log_warning(
                f"Business validation failed. LPN={payload.request.lpn}",
                method,
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response.model_dump(
                by_alias=True,
            ),
        )

    except Exception as ex:

        logger.log_error(
            f"Unexpected error: {str(ex)}",
            method,
        )

        error_response = ApiResponse.create_error(
            error_message=f"Unexpected error: {str(ex)}",
            meta=None,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(
                by_alias=True,
            ),
        )


@label_router.get("/history", response_model=ApiResponse)
async def get_history():

    method = "get_history"

    logger.log_information("History request received", method)

    try:

        response = label_service.get_print_history()

        logger.log_information(
            "History returned successfully",
            method,
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response.model_dump(
                by_alias=True,
            ),
        )

    except Exception as ex:

        logger.log_error(
            f"Unexpected error: {str(ex)}",
            method,
        )

        error_response = ApiResponse.create_error(
            error_message=str(ex),
            meta=None,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(
                by_alias=True,
            ),
        )
