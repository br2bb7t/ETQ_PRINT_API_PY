from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from domain.models.base import Base


class Product(Base):

    __tablename__ = "PRODUCT"

    PRODUCT_CODE = Column(
        String(50),
        primary_key=True,
    )

    PRODUCT_DESCRIPTION = Column(
        String(200),
        nullable=False,
    )

    ORDERS = relationship(
        "OrderProduct",
        back_populates="PRODUCT",
    )

    INVENTORIES = relationship(
        "Inventory",
        back_populates="PRODUCT",
    )
