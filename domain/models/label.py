from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from domain.models.base import Base


class Label(Base):

    __tablename__ = "LABEL"

    ETQ_ID = Column(
        String(50),
        primary_key=True,
    )

    LPN_ID = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    REQUEST_ID = Column(
        String(50),
        ForeignKey("PRINT_ORDER.REQUEST_ID"),
        nullable=False,
    )

    TEMPLATE_CODE = Column(String(100))

    IS_PRE_GENERATED = Column(
        Integer,
        default=1,
        nullable=False,
    )

    ZPL = Column(Text)

    ORDER = relationship(
        "PrintOrder",
        back_populates="LABELS",
    )

    AUDITS = relationship(
        "AuditPrint",
        back_populates="LABEL",
    )
