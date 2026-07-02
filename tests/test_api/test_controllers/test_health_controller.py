import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from api.response.api_response import ApiResponse


@pytest.mark.asyncio
@patch("api.controllers.health_controller.get_db_session")
@patch("api.controllers.health_controller.logger.log_information")
async def test_health_check_success(mock_log_info, mock_get_db_session):
    """
    Verify successful database health check.
    """

    from api.controllers.health_controller import health_check

    mock_session = MagicMock()

    mock_session.execute.return_value = None

    mock_get_db_session.return_value.__enter__.return_value = mock_session

    response = await health_check()

    assert isinstance(response, ApiResponse)

    assert response.is_successful is True
    assert response.is_error is False

    assert response.result == "Database connection successful"

    assert response.meta is None

    mock_session.execute.assert_called_once()

    mock_log_info.assert_called_once()


@pytest.mark.asyncio
@patch("api.controllers.health_controller.get_db_session")
@patch("api.controllers.health_controller.logger.log_error")
async def test_health_check_failure(mock_log_error, mock_get_db_session):
    """
    Verify 503 response when database connection fails.
    """

    from api.controllers.health_controller import health_check

    mock_session = MagicMock()

    mock_session.execute.side_effect = OperationalError(
        "SELECT 1",
        {},
        Exception("Database unavailable"),
    )

    mock_get_db_session.return_value.__enter__.return_value = mock_session

    response = await health_check()

    assert isinstance(response, JSONResponse)

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

    body = json.loads(response.body.decode("utf-8"))

    assert body["isSuccessful"] is False
    assert body["isError"] is True
    assert body["errorMessage"] == "Database connection failed"

    assert body["result"] is None
    assert body["meta"] is None

    mock_log_error.assert_called_once()
