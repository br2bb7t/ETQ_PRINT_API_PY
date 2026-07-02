from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from domain.models.base import Base


class Inventory(Base):

    __tablename__ = "INVENTORY"

    PRODUCT_CODE = Column(
        String(50),
        ForeignKey("PRODUCT.PRODUCT_CODE"),
        primary_key=True,
    )

    ZONE = Column(
        String(100),
        primary_key=True,
    )

    AVAILABLE_QTY = Column(
        Numeric(10, 2),
        nullable=False,
    )

    IS_SUPPLIED = Column(
        Integer,
        nullable=False,
        default=0,
    )

    PRODUCT = relationship(
        "Product",
        back_populates="INVENTORIES",
    )
