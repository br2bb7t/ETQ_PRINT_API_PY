from datetime import datetime

from domain.models.audit_print import AuditPrint
from domain.models.inventory import Inventory
from domain.models.label import Label
from domain.models.order_product import OrderProduct
from domain.models.print_order import PrintOrder
from domain.models.product import Product
from infrastructure.database.db_context import get_db_session


class SeedDataInitializer:

    @staticmethod
    def seed():

        with get_db_session() as session:

            if session.query(PrintOrder).count() > 0:
                return

            # PRODUCTOS
            # ==========================================================

            session.add_all(
                [
                    Product(
                        PRODUCT_CODE="SKU001",
                        PRODUCT_DESCRIPTION="Martillo 16oz",
                    ),
                    Product(
                        PRODUCT_CODE="SKU002",
                        PRODUCT_DESCRIPTION="Guantes de seguridad",
                    ),
                    Product(
                        PRODUCT_CODE="SKU003",
                        PRODUCT_DESCRIPTION="Casco industrial",
                    ),
                    Product(
                        PRODUCT_CODE="SKU004",
                        PRODUCT_DESCRIPTION="Botas de seguridad",
                    ),
                ]
            )

            session.flush()

            # INVENTARIO
            # ==========================================================

            session.add_all(
                [
                    # Inventario válido
                    Inventory(
                        PRODUCT_CODE="SKU001",
                        ZONE="ZONA-PICKING-A",
                        AVAILABLE_QTY=100,
                        IS_SUPPLIED=1,
                    ),
                    Inventory(
                        PRODUCT_CODE="SKU002",
                        ZONE="ZONA-PICKING-A",
                        AVAILABLE_QTY=50,
                        IS_SUPPLIED=1,
                    ),
                    # Producto NO abastecido
                    Inventory(
                        PRODUCT_CODE="SKU003",
                        ZONE="ZONA-PICKING-A",
                        AVAILABLE_QTY=100,
                        IS_SUPPLIED=0,
                    ),
                    # Inventario insuficiente
                    Inventory(
                        PRODUCT_CODE="SKU004",
                        ZONE="ZONA-PICKING-A",
                        AVAILABLE_QTY=2,
                        IS_SUPPLIED=1,
                    ),
                    # Inventario en otra zona
                    Inventory(
                        PRODUCT_CODE="SKU001",
                        ZONE="ZONA-PICKING-B",
                        AVAILABLE_QTY=20,
                        IS_SUPPLIED=1,
                    ),
                ]
            )

            # CASO 1 - IMPRESIÓN EXITOSA
            # LPN: olpn12345
            # ==========================================================

            session.add(
                PrintOrder(
                    REQUEST_ID="REQ-001",
                    REQUEST_DATE_TIME=datetime.now(),
                    REQUESTED_BY="usuario.operacion",
                    ZONE="ZONA-PICKING-A",
                    DOCUMENT_TYPE="NOTA_PEDIDO",
                    DOCUMENT_NUMBER="NP-001",
                    DOCUMENT_STATUS="LIBERADA",
                )
            )

            session.add(
                Label(
                    ETQ_ID="ETQ-001",
                    REQUEST_ID="REQ-001",
                    LPN_ID="olpn12345",
                    IS_PRE_GENERATED=1,
                    TEMPLATE_CODE="TPL-STD",
                    ZPL="^XA^FO50,50^FDPRINT OK^FS^XZ",
                )
            )

            session.add(
                OrderProduct(
                    REQUEST_ID="REQ-001",
                    PRODUCT_CODE="SKU001",
                    REQUESTED_QTY=2,
                    UOM="UND",
                )
            )

            # CASO 2 - REIMPRESIÓN
            # LPN: olpn22222
            # ==========================================================

            session.add(
                PrintOrder(
                    REQUEST_ID="REQ-002",
                    REQUEST_DATE_TIME=datetime.now(),
                    REQUESTED_BY="usuario.operacion",
                    ZONE="ZONA-PICKING-A",
                    DOCUMENT_TYPE="NOTA_PEDIDO",
                    DOCUMENT_NUMBER="NP-002",
                    DOCUMENT_STATUS="LIBERADA",
                )
            )

            session.add(
                Label(
                    ETQ_ID="ETQ-002",
                    REQUEST_ID="REQ-002",
                    LPN_ID="olpn22222",
                    IS_PRE_GENERATED=1,
                    TEMPLATE_CODE="TPL-STD",
                    ZPL="^XA^FO50,50^FDREPRINT^FS^XZ",
                )
            )

            session.add(
                OrderProduct(
                    REQUEST_ID="REQ-002",
                    PRODUCT_CODE="SKU002",
                    REQUESTED_QTY=1,
                    UOM="UND",
                )
            )

            session.add(
                AuditPrint(
                    ETQ_ID="ETQ-002",
                    REQUEST_ID="REQ-002",
                    LPN_ID="olpn22222",
                    USER_NAME="SYSTEM",
                    EVENT_TYPE="PRINT",
                    RESULT="SUCCESS",
                )
            )

            # CASO 3 - INVENTARIO INSUFICIENTE
            # LPN: olpn33333
            # ==========================================================

            session.add(
                PrintOrder(
                    REQUEST_ID="REQ-003",
                    REQUEST_DATE_TIME=datetime.now(),
                    REQUESTED_BY="usuario.operacion",
                    ZONE="ZONA-PICKING-A",
                    DOCUMENT_TYPE="NOTA_PEDIDO",
                    DOCUMENT_NUMBER="NP-003",
                    DOCUMENT_STATUS="LIBERADA",
                )
            )

            session.add(
                Label(
                    ETQ_ID="ETQ-003",
                    REQUEST_ID="REQ-003",
                    LPN_ID="olpn33333",
                    IS_PRE_GENERATED=1,
                    TEMPLATE_CODE="TPL-STD",
                    ZPL="^XA^FO50,50^FDNO INVENTORY^FS^XZ",
                )
            )

            session.add(
                OrderProduct(
                    REQUEST_ID="REQ-003",
                    PRODUCT_CODE="SKU004",
                    REQUESTED_QTY=10,
                    UOM="UND",
                )
            )

            # CASO 4 - DOCUMENTO ANULADO
            # LPN: olpn44444
            # ==========================================================

            session.add(
                PrintOrder(
                    REQUEST_ID="REQ-004",
                    REQUEST_DATE_TIME=datetime.now(),
                    REQUESTED_BY="usuario.operacion",
                    ZONE="ZONA-PICKING-A",
                    DOCUMENT_TYPE="NOTA_PEDIDO",
                    DOCUMENT_NUMBER="NP-004",
                    DOCUMENT_STATUS="ANULADA",
                )
            )

            session.add(
                Label(
                    ETQ_ID="ETQ-004",
                    REQUEST_ID="REQ-004",
                    LPN_ID="olpn44444",
                    IS_PRE_GENERATED=1,
                    TEMPLATE_CODE="TPL-STD",
                    ZPL="^XA^FO50,50^FDCANCELLED^FS^XZ",
                )
            )

            # CASO 5 - DOCUMENTO DEVUELTO
            # LPN: olpn55555
            # ==========================================================

            session.add(
                PrintOrder(
                    REQUEST_ID="REQ-005",
                    REQUEST_DATE_TIME=datetime.now(),
                    REQUESTED_BY="usuario.operacion",
                    ZONE="ZONA-PICKING-A",
                    DOCUMENT_TYPE="NOTA_PEDIDO",
                    DOCUMENT_NUMBER="NP-005",
                    DOCUMENT_STATUS="DEVUELTA",
                )
            )

            session.add(
                Label(
                    ETQ_ID="ETQ-005",
                    REQUEST_ID="REQ-005",
                    LPN_ID="olpn55555",
                    IS_PRE_GENERATED=1,
                    TEMPLATE_CODE="TPL-STD",
                    ZPL="^XA^FO50,50^FDRETURNED^FS^XZ",
                )
            )

            # CASO 6 - PRODUCTO NO ABASTECIDO
            # LPN: olpn66666
            # ==========================================================

            session.add(
                PrintOrder(
                    REQUEST_ID="REQ-006",
                    REQUEST_DATE_TIME=datetime.now(),
                    REQUESTED_BY="usuario.operacion",
                    ZONE="ZONA-PICKING-A",
                    DOCUMENT_TYPE="NOTA_PEDIDO",
                    DOCUMENT_NUMBER="NP-006",
                    DOCUMENT_STATUS="LIBERADA",
                )
            )

            session.add(
                Label(
                    ETQ_ID="ETQ-006",
                    REQUEST_ID="REQ-006",
                    LPN_ID="olpn66666",
                    IS_PRE_GENERATED=1,
                    TEMPLATE_CODE="TPL-STD",
                    ZPL="^XA^FO50,50^FDNOT SUPPLIED^FS^XZ",
                )
            )

            session.add(
                OrderProduct(
                    REQUEST_ID="REQ-006",
                    PRODUCT_CODE="SKU003",
                    REQUESTED_QTY=1,
                    UOM="UND",
                )
            )

            # CASO 7 - ZONA SIN INVENTARIO
            # LPN: olpn77777
            # ==========================================================

            session.add(
                PrintOrder(
                    REQUEST_ID="REQ-007",
                    REQUEST_DATE_TIME=datetime.now(),
                    REQUESTED_BY="usuario.operacion",
                    ZONE="ZONA-PICKING-C",
                    DOCUMENT_TYPE="NOTA_PEDIDO",
                    DOCUMENT_NUMBER="NP-007",
                    DOCUMENT_STATUS="LIBERADA",
                )
            )

            session.add(
                Label(
                    ETQ_ID="ETQ-007",
                    REQUEST_ID="REQ-007",
                    LPN_ID="olpn77777",
                    IS_PRE_GENERATED=1,
                    TEMPLATE_CODE="TPL-STD",
                    ZPL="^XA^FO50,50^FDZONE ERROR^FS^XZ",
                )
            )

            session.add(
                OrderProduct(
                    REQUEST_ID="REQ-007",
                    PRODUCT_CODE="SKU001",
                    REQUESTED_QTY=1,
                    UOM="UND",
                )
            )

            # CASO 8 - MULTIPRODUCTO EXITOSO
            # LPN: olpn88888
            # ==========================================================

            session.add(
                PrintOrder(
                    REQUEST_ID="REQ-008",
                    REQUEST_DATE_TIME=datetime.now(),
                    REQUESTED_BY="usuario.operacion",
                    ZONE="ZONA-PICKING-A",
                    DOCUMENT_TYPE="NOTA_PEDIDO",
                    DOCUMENT_NUMBER="NP-008",
                    DOCUMENT_STATUS="LIBERADA",
                )
            )

            session.add(
                Label(
                    ETQ_ID="ETQ-008",
                    REQUEST_ID="REQ-008",
                    LPN_ID="olpn88888",
                    IS_PRE_GENERATED=1,
                    TEMPLATE_CODE="TPL-STD",
                    ZPL="^XA^FO50,50^FDMULTI PRODUCT^FS^XZ",
                )
            )

            session.add_all(
                [
                    OrderProduct(
                        REQUEST_ID="REQ-008",
                        PRODUCT_CODE="SKU001",
                        REQUESTED_QTY=2,
                        UOM="UND",
                    ),
                    OrderProduct(
                        REQUEST_ID="REQ-008",
                        PRODUCT_CODE="SKU002",
                        REQUESTED_QTY=3,
                        UOM="UND",
                    ),
                ]
            )

            session.commit()

            print("Seed data loaded successfully")
