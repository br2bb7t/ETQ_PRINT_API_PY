from domain.models.audit_print import AuditPrint
from domain.models.base import Base
from domain.models.inventory import Inventory
from domain.models.label import Label
from domain.models.order_product import OrderProduct

# Import all models
from domain.models.print_order import PrintOrder
from domain.models.product import Product
from infrastructure.database.db_context import engine


class DatabaseInitializer:

    @staticmethod
    def initialize():

        Base.metadata.create_all(bind=engine)
