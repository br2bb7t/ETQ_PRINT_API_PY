from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from domain.models.base import Base


class PrintOrder(Base):

    __tablename__ = "PRINT_ORDER"

    REQUEST_ID = Column(String(50), primary_key=True)

    REQUEST_DATE_TIME = Column(DateTime, nullable=False)

    REQUESTED_BY = Column(String(100), nullable=False)

    ZONE = Column(String(100), nullable=False)

    DOCUMENT_TYPE = Column(String(50), nullable=False)

    DOCUMENT_NUMBER = Column(String(50), nullable=False)

    DOCUMENT_STATUS = Column(String(20), nullable=False)

    REPRINT_REASON = Column(String(500))

    LABELS = relationship(
        "Label",
        back_populates="ORDER",
    )

    PRODUCTS = relationship(
        "OrderProduct",
        back_populates="ORDER",
    )
