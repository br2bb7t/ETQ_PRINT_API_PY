from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.controllers.label_controller import label_router
from api.response.api_response import ApiResponse

app = FastAPI()
app.include_router(label_router)

client = TestClient(app)


@patch("api.controllers.label_controller.label_service")
def test_print_label_success(mock_service):

    mock_service.print_label.return_value = ApiResponse.create_successful(
        result={
            "idEtiqueta": "ETQ-10001",
            "purchaseOrder": "NP-001",
            "tcOrderId": "REQ-001",
            "products": [],
            "zpl": "^XA^XZ",
            "isReprint": False,
        },
        meta=None,
        messages=None,
    )

    response = client.post(
        "/labels/print",
        json={
            "request": {
                "lpn": "olpn12345",
            }
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["isSuccessful"] is True
    assert body["result"]["idEtiqueta"] == "ETQ-10001"


@patch("api.controllers.label_controller.label_service")
def test_print_label_business_error(mock_service):

    mock_service.print_label.return_value = ApiResponse.create_error(
        error_message="LPN not found",
        meta=None,
    )

    response = client.post(
        "/labels/print",
        json={
            "request": {
                "lpn": "INVALID",
            }
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["isSuccessful"] is False
    assert body["errorMessage"] == "LPN not found"


@patch("api.controllers.label_controller.label_service")
def test_print_label_unexpected_error(mock_service):

    mock_service.print_label.side_effect = Exception("Database connection failed")

    response = client.post(
        "/labels/print",
        json={
            "request": {
                "lpn": "olpn12345",
            }
        },
    )

    assert response.status_code == 500

    body = response.json()

    assert body["isSuccessful"] is False
    assert "Database connection failed" in body["errorMessage"]


@patch("api.controllers.label_controller.label_service")
def test_get_history_success(mock_service):

    mock_service.get_print_history.return_value = ApiResponse.create_successful(
        result=[
            {
                "etqId": "ETQ-10001",
                "eventType": "PRINT",
            }
        ],
        meta={
            "totalItems": 1,
            "status": "SUCCESS",
        },
        messages=None,
    )

    response = client.get("/labels/history")

    assert response.status_code == 200

    body = response.json()

    assert body["isSuccessful"] is True
    assert len(body["result"]) == 1


@patch("api.controllers.label_controller.label_service")
def test_get_history_unexpected_error(mock_service):

    mock_service.get_print_history.side_effect = Exception("Unexpected error")

    response = client.get("/labels/history")

    assert response.status_code == 500

    body = response.json()

    assert body["isSuccessful"] is False
    assert "Unexpected error" in body["errorMessage"]
