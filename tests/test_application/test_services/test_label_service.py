from unittest.mock import Mock

import pytest

from application.services.label_service import LabelService


@pytest.fixture
def service():

    service = LabelService()

    service.repository = Mock()

    return service


def test_print_label_success(service):

    service.repository.get_label_by_lpn.return_value = {
        "ETQ_ID": "ETQ-10001",
        "LPN_ID": "olpn12345",
        "REQUEST_ID": "REQ-001",
        "ZPL": "^XA^XZ",
    }

    service.repository.get_order.return_value = {
        "REQUEST_ID": "REQ-001",
        "DOCUMENT_NUMBER": "NP-001",
        "DOCUMENT_STATUS": "LIBERADA",
        "ZONE": "ZONA-PICKING-A",
    }

    service.repository.get_order_products.return_value = [
        {
            "PRODUCT_CODE": "SKU001",
            "REQUESTED_QTY": 2,
            "UOM": "UND",
        }
    ]

    service.repository.get_inventory.return_value = {
        "PRODUCT_CODE": "SKU001",
        "AVAILABLE_QTY": 100,
        "ZONE": "ZONA-PICKING-A",
        "IS_SUPPLIED": True,
    }

    service.repository.exists_previous_print.return_value = False

    response = service.print_label("olpn12345")

    assert response.is_successful is True
    assert response.result["idEtiqueta"] == "ETQ-10001"
    assert response.result["isReprint"] is False


def test_print_label_reprint(service):

    service.repository.get_label_by_lpn.return_value = {
        "ETQ_ID": "ETQ-10002",
        "LPN_ID": "olpn22222",
        "REQUEST_ID": "REQ-002",
        "ZPL": "^XA^XZ",
    }

    service.repository.get_order.return_value = {
        "REQUEST_ID": "REQ-002",
        "DOCUMENT_NUMBER": "NP-002",
        "DOCUMENT_STATUS": "LIBERADA",
        "ZONE": "ZONA-PICKING-A",
    }

    service.repository.get_order_products.return_value = [
        {
            "PRODUCT_CODE": "SKU002",
            "REQUESTED_QTY": 1,
            "UOM": "UND",
        }
    ]

    service.repository.get_inventory.return_value = {
        "PRODUCT_CODE": "SKU002",
        "AVAILABLE_QTY": 50,
        "ZONE": "ZONA-PICKING-A",
        "IS_SUPPLIED": True,
    }

    service.repository.exists_previous_print.return_value = True

    response = service.print_label("olpn22222")

    assert response.is_successful is True
    assert response.result["isReprint"] is True


def test_lpn_not_found(service):

    service.repository.get_label_by_lpn.return_value = None

    response = service.print_label("INVALID")

    assert response.is_successful is False
    assert response.error_message == "LPN not found"


def test_order_not_found(service):

    service.repository.get_label_by_lpn.return_value = {
        "ETQ_ID": "ETQ-1",
        "REQUEST_ID": "REQ-1",
        "LPN_ID": "LPN-1",
        "ZPL": "ZPL",
    }

    service.repository.get_order.return_value = None

    response = service.print_label("LPN-1")

    assert response.is_successful is False
    assert response.error_message == "Order not found"


def test_order_cancelled(service):

    service.repository.get_label_by_lpn.return_value = {
        "ETQ_ID": "ETQ-1",
        "REQUEST_ID": "REQ-1",
        "LPN_ID": "LPN-1",
        "ZPL": "ZPL",
    }

    service.repository.get_order.return_value = {
        "REQUEST_ID": "REQ-1",
        "DOCUMENT_NUMBER": "NP-001",
        "DOCUMENT_STATUS": "ANULADA",
        "ZONE": "A",
    }

    response = service.print_label("LPN-1")

    assert response.is_successful is False


def test_order_without_products(service):

    service.repository.get_label_by_lpn.return_value = {
        "ETQ_ID": "ETQ-1",
        "REQUEST_ID": "REQ-1",
        "LPN_ID": "LPN-1",
        "ZPL": "ZPL",
    }

    service.repository.get_order.return_value = {
        "REQUEST_ID": "REQ-1",
        "DOCUMENT_NUMBER": "NP-001",
        "DOCUMENT_STATUS": "LIBERADA",
        "ZONE": "A",
    }

    service.repository.get_order_products.return_value = []

    response = service.print_label("LPN-1")

    assert response.is_successful is False
    assert response.error_message == "Order has no products"


def test_inventory_not_found(service):

    service.repository.get_label_by_lpn.return_value = {
        "ETQ_ID": "ETQ-1",
        "REQUEST_ID": "REQ-1",
        "LPN_ID": "LPN-1",
        "ZPL": "ZPL",
    }

    service.repository.get_order.return_value = {
        "REQUEST_ID": "REQ-1",
        "DOCUMENT_NUMBER": "NP-001",
        "DOCUMENT_STATUS": "LIBERADA",
        "ZONE": "A",
    }

    service.repository.get_order_products.return_value = [
        {
            "PRODUCT_CODE": "SKU001",
            "REQUESTED_QTY": 2,
            "UOM": "UND",
        }
    ]

    service.repository.get_inventory.return_value = None

    response = service.print_label("LPN-1")

    assert response.is_successful is False


def test_insufficient_inventory(service):

    service.repository.get_label_by_lpn.return_value = {
        "ETQ_ID": "ETQ-1",
        "REQUEST_ID": "REQ-1",
        "LPN_ID": "LPN-1",
        "ZPL": "ZPL",
    }

    service.repository.get_order.return_value = {
        "REQUEST_ID": "REQ-1",
        "DOCUMENT_NUMBER": "NP-001",
        "DOCUMENT_STATUS": "LIBERADA",
        "ZONE": "A",
    }

    service.repository.get_order_products.return_value = [
        {
            "PRODUCT_CODE": "SKU001",
            "REQUESTED_QTY": 10,
            "UOM": "UND",
        }
    ]

    service.repository.get_inventory.return_value = {
        "PRODUCT_CODE": "SKU001",
        "AVAILABLE_QTY": 2,
        "ZONE": "A",
        "IS_SUPPLIED": True,
    }

    response = service.print_label("LPN-1")

    assert response.is_successful is False


def test_product_not_supplied(service):

    service.repository.get_label_by_lpn.return_value = {
        "ETQ_ID": "ETQ-1",
        "REQUEST_ID": "REQ-1",
        "LPN_ID": "LPN-1",
        "ZPL": "ZPL",
    }

    service.repository.get_order.return_value = {
        "REQUEST_ID": "REQ-1",
        "DOCUMENT_NUMBER": "NP-001",
        "DOCUMENT_STATUS": "LIBERADA",
        "ZONE": "A",
    }

    service.repository.get_order_products.return_value = [
        {
            "PRODUCT_CODE": "SKU001",
            "REQUESTED_QTY": 1,
            "UOM": "UND",
        }
    ]

    service.repository.get_inventory.return_value = {
        "PRODUCT_CODE": "SKU001",
        "AVAILABLE_QTY": 10,
        "ZONE": "A",
        "IS_SUPPLIED": False,
    }

    response = service.print_label("LPN-1")

    assert response.is_successful is False


def test_get_print_history(service):

    service.repository.get_print_history.return_value = [
        {
            "etqId": "ETQ-1",
            "eventType": "PRINT",
        }
    ]

    response = service.get_print_history()

    assert response.is_successful is True
    assert len(response.result) == 1


def test_print_label_unexpected_exception():

    service = LabelService()

    repository_mock = Mock()

    repository_mock.get_label_by_lpn.side_effect = Exception("Database connection error")

    service.repository = repository_mock

    response = service.print_label("olpn12345")

    assert response.is_successful is False
    assert response.is_error is True
    assert response.error_message == "Database connection error"


def test_get_print_history_unexpected_exception():

    service = LabelService()

    repository_mock = Mock()

    repository_mock.get_print_history.side_effect = Exception("History query failed")

    service.repository = repository_mock

    response = service.get_print_history()

    assert response.is_successful is False
    assert response.is_error is True
    assert response.error_message == "History query failed"
