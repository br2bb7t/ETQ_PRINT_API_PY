from domain.models.audit_print import AuditPrint
from domain.models.inventory import Inventory
from domain.models.label import Label
from domain.models.order_product import OrderProduct
from domain.models.print_order import PrintOrder
from infrastructure.logging.LoggerImplements import LoggerImplements


class LabelRepository:

    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory
        self.logger = LoggerImplements("LabelRepository")

    def get_label_by_lpn(self, lpn: str):

        method = "get_label_by_lpn"

        try:

            with self.db_session_factory() as session:

                label = session.query(Label).filter(Label.LPN_ID == lpn).first()

                if not label:
                    return None

                return {
                    "ETQ_ID": label.ETQ_ID,
                    "LPN_ID": label.LPN_ID,
                    "REQUEST_ID": label.REQUEST_ID,
                    "ZPL": label.ZPL,
                }

        except Exception as ex:
            self.logger.log_error(f"Error in {method}: {str(ex)}", method)
            raise

    def get_order(self, request_id: str):

        method = "get_order"

        try:

            with self.db_session_factory() as session:

                order = session.query(PrintOrder).filter(PrintOrder.REQUEST_ID == request_id).first()

                if not order:
                    return None

                return {
                    "REQUEST_ID": order.REQUEST_ID,
                    "DOCUMENT_NUMBER": order.DOCUMENT_NUMBER,
                    "DOCUMENT_STATUS": order.DOCUMENT_STATUS,
                    "ZONE": order.ZONE,
                }

        except Exception as ex:
            self.logger.log_error(f"Error in {method}: {str(ex)}", method)
            raise

    def get_order_products(self, request_id: str):

        method = "get_order_products"

        try:

            with self.db_session_factory() as session:

                products = session.query(OrderProduct).filter(OrderProduct.REQUEST_ID == request_id).all()

                return [
                    {
                        "PRODUCT_CODE": p.PRODUCT_CODE,
                        "REQUESTED_QTY": float(p.REQUESTED_QTY),
                        "UOM": p.UOM,
                    }
                    for p in products
                ]

        except Exception as ex:
            self.logger.log_error(f"Error in {method}: {str(ex)}", method)
            raise

    def get_inventory(self, product_code: str, zone: str):

        method = "get_inventory"

        try:

            with self.db_session_factory() as session:

                inventory = (
                    session.query(Inventory)
                    .filter(
                        Inventory.PRODUCT_CODE == product_code,
                        Inventory.ZONE == zone,
                    )
                    .first()
                )

                if not inventory:
                    return None

                return {
                    "PRODUCT_CODE": inventory.PRODUCT_CODE,
                    "AVAILABLE_QTY": float(inventory.AVAILABLE_QTY),
                    "ZONE": inventory.ZONE,
                    "IS_SUPPLIED": bool(inventory.IS_SUPPLIED),
                }

        except Exception as ex:
            self.logger.log_error(f"Error in {method}: {str(ex)}", method)
            raise

    def exists_previous_print(self, etq_id: str):

        method = "exists_previous_print"

        try:

            with self.db_session_factory() as session:

                count = session.query(AuditPrint).filter(AuditPrint.ETQ_ID == etq_id).count()

                return count > 0

        except Exception as ex:
            self.logger.log_error(f"Error in {method}: {str(ex)}", method)
            raise

    def save_print_audit(
        self,
        etq_id: str,
        request_id: str,
        lpn_id: str,
        event_type: str,
        result: str,
        user_name: str,
        reason: str | None = None,
    ):

        method = "save_print_audit"

        try:

            with self.db_session_factory() as session:

                audit = AuditPrint(
                    ETQ_ID=etq_id,
                    REQUEST_ID=request_id,
                    LPN_ID=lpn_id,
                    USER_NAME=user_name,
                    EVENT_TYPE=event_type,
                    RESULT=result,
                    REASON=reason,
                )

                session.add(audit)

        except Exception as ex:
            self.logger.log_error(f"Error in {method}: {str(ex)}", method)
            raise

    def save_rejection_audit(
        self,
        etq_id: str,
        request_id: str,
        lpn_id: str,
        user_name: str,
        reason: str,
    ):

        self.save_print_audit(
            etq_id=etq_id,
            request_id=request_id,
            lpn_id=lpn_id,
            event_type="REJECTED",
            result="FAILED",
            user_name=user_name,
            reason=reason,
        )

    def get_print_history(self):

        method = "get_print_history"

        try:

            with self.db_session_factory() as session:

                audits = session.query(AuditPrint).order_by(AuditPrint.AUDIT_ID.desc()).all()

                return [
                    {
                        "etqId": a.ETQ_ID,
                        "requestId": a.REQUEST_ID,
                        "lpnId": a.LPN_ID,
                        "user": a.USER_NAME,
                        "eventType": a.EVENT_TYPE,
                        "result": a.RESULT,
                        "reason": a.REASON,
                        "createdAt": str(a.CREATED_AT),
                    }
                    for a in audits
                ]

        except Exception as ex:
            self.logger.log_error(f"Error in {method}: {str(ex)}", method)
            raise
