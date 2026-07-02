from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from domain.models.base import Base


class OrderProduct(Base):

    __tablename__ = "ORDER_PRODUCT"

    REQUEST_ID = Column(
        String(50),
        ForeignKey("PRINT_ORDER.REQUEST_ID"),
        primary_key=True,
    )

    PRODUCT_CODE = Column(
        String(50),
        ForeignKey("PRODUCT.PRODUCT_CODE"),
        primary_key=True,
    )

    REQUESTED_QTY = Column(
        Numeric(10, 2),
        nullable=False,
    )

    UOM = Column(
        String(20),
        nullable=False,
    )

    ORDER = relationship(
        "PrintOrder",
        back_populates="PRODUCTS",
    )

    PRODUCT = relationship(
        "Product",
        back_populates="ORDERS",
    )
