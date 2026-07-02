import time

from api.response.api_response import ApiResponse
from domain.repositories.label_repository import LabelRepository
from infrastructure.database.db_context import get_db_session
from infrastructure.logging.LoggerImplements import LoggerImplements


class LabelService:

    def __init__(self):
        self.logger = LoggerImplements("LabelService")
        self.repository = LabelRepository(get_db_session)

    def print_label(self, lpn: str, user: str = "SYSTEM", reason: str | None = None) -> ApiResponse:

        method = "print_label"

        start_time = time.perf_counter()

        self.logger.log_information(f"Starting print process. LPN={lpn}", method)

        try:

            label = self.repository.get_label_by_lpn(lpn)

            if not label:

                self.logger.log_warning(f"LPN not found. LPN={lpn}", method)

                return ApiResponse.create_error(
                    error_message="LPN not found",
                    meta=None,
                )

            order = self.repository.get_order(label["REQUEST_ID"])

            if not order:

                self.logger.log_warning(
                    f"Order not found. REQUEST_ID={label['REQUEST_ID']}",
                    method,
                )

                return ApiResponse.create_error(
                    error_message="Order not found",
                    meta=None,
                )

            invalid_status = [
                "ANULADA",
                "DEVUELTA",
            ]

            if order["DOCUMENT_STATUS"] in invalid_status:

                self.logger.log_warning(
                    f"Order rejected. Status={order['DOCUMENT_STATUS']}",
                    method,
                )

                self.repository.save_rejection_audit(
                    label["ETQ_ID"],
                    label["REQUEST_ID"],
                    label["LPN_ID"],
                    user,
                    f"Document status {order['DOCUMENT_STATUS']}",
                )

                return ApiResponse.create_error(
                    error_message=f"Document status {order['DOCUMENT_STATUS']} not allowed",
                    meta=None,
                )

            products = self.repository.get_order_products(order["REQUEST_ID"])

            if not products:

                self.logger.log_warning(
                    f"Order has no products. REQUEST_ID={order['REQUEST_ID']}",
                    method,
                )

                return ApiResponse.create_error(
                    error_message="Order has no products",
                    meta=None,
                )

            validated_products = []

            for product in products:

                self.logger.log_information(
                    f"Validating SKU={product['PRODUCT_CODE']}",
                    method,
                )

                inventory = self.repository.get_inventory(
                    product["PRODUCT_CODE"],
                    order["ZONE"],
                )

                if not inventory:

                    self.logger.log_warning(
                        (f"Inventory not found. " f"SKU={product['PRODUCT_CODE']} " f"ZONE={order['ZONE']}"),
                        method,
                    )

                    self.repository.save_rejection_audit(
                        label["ETQ_ID"],
                        label["REQUEST_ID"],
                        label["LPN_ID"],
                        user,
                        f"Inventory not found for {product['PRODUCT_CODE']}",
                    )

                    return ApiResponse.create_error(
                        error_message=(f"Inventory not found for " f"{product['PRODUCT_CODE']}"),
                        meta=None,
                    )

                if not inventory["IS_SUPPLIED"]:

                    self.logger.log_warning(
                        f"Product not supplied. SKU={product['PRODUCT_CODE']}",
                        method,
                    )

                    self.repository.save_rejection_audit(
                        label["ETQ_ID"],
                        label["REQUEST_ID"],
                        label["LPN_ID"],
                        user,
                        f"Product {product['PRODUCT_CODE']} is not supplied",
                    )

                    return ApiResponse.create_error(
                        error_message=(f"Product {product['PRODUCT_CODE']} " f"is not supplied"),
                        meta=None,
                    )

                if inventory["AVAILABLE_QTY"] < product["REQUESTED_QTY"]:

                    self.logger.log_warning(
                        (
                            f"Insufficient inventory. "
                            f"SKU={product['PRODUCT_CODE']} "
                            f"REQUESTED={product['REQUESTED_QTY']} "
                            f"AVAILABLE={inventory['AVAILABLE_QTY']}"
                        ),
                        method,
                    )

                    self.repository.save_rejection_audit(
                        label["ETQ_ID"],
                        label["REQUEST_ID"],
                        label["LPN_ID"],
                        user,
                        f"Insufficient inventory for {product['PRODUCT_CODE']}",
                    )

                    return ApiResponse.create_error(
                        error_message=(f"Insufficient inventory for " f"{product['PRODUCT_CODE']}"),
                        meta=None,
                    )

                validated_products.append(
                    {
                        "sku": product["PRODUCT_CODE"],
                        "requestedQty": product["REQUESTED_QTY"],
                        "availableQty": inventory["AVAILABLE_QTY"],
                    }
                )

            is_reprint = self.repository.exists_previous_print(label["ETQ_ID"])

            if is_reprint:

                self.logger.log_warning(
                    f"Reprint detected. ETQ_ID={label['ETQ_ID']}",
                    method,
                )

            self.repository.save_print_audit(
                etq_id=label["ETQ_ID"],
                request_id=label["REQUEST_ID"],
                lpn_id=label["LPN_ID"],
                event_type="REPRINT" if is_reprint else "PRINT",
                result="SUCCESS",
                user_name=user,
                reason=reason,
            )

            self.logger.log_information(
                f"Label printed successfully. ETQ_ID={label['ETQ_ID']}",
                method,
            )

            result = {
                "idEtiqueta": label["ETQ_ID"],
                "purchaseOrder": order["DOCUMENT_NUMBER"],
                "tcOrderId": order["REQUEST_ID"],
                "products": validated_products,
                "zpl": label["ZPL"],
                "isReprint": is_reprint,
            }

            return ApiResponse.create_successful(
                result=result,
                meta=None,
                messages=None,
            )

        except Exception as ex:
            self.logger.log_error(str(ex), method)
            return ApiResponse.create_error(error_message=str(ex), meta=None)

        finally:
            duration = round(time.perf_counter() - start_time, 4)
            self.logger.log_information(f"Execution completed in {duration}s", method)

    def get_print_history(self):

        method = "get_print_history"

        self.logger.log_information("Retrieving print history", method)

        try:

            history = self.repository.get_print_history()

            self.logger.log_information(
                f"History records found: {len(history)}",
                method,
            )

            return ApiResponse.create_successful(
                result=history,
                meta={
                    "totalItems": len(history),
                    "status": "SUCCESS",
                },
                messages=None,
            )

        except Exception as ex:
            self.logger.log_error(str(ex), method)
            return ApiResponse.create_error(error_message=str(ex), meta=None)
