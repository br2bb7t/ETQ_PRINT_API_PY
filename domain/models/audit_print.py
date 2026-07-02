from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from domain.models.base import Base


class AuditPrint(Base):

    __tablename__ = "AUDIT_PRINT"

    AUDIT_ID = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    ETQ_ID = Column(
        String(50),
        ForeignKey("LABEL.ETQ_ID"),
        nullable=False,
    )

    REQUEST_ID = Column(String(50))

    LPN_ID = Column(String(50))

    USER_NAME = Column(String(100))

    EVENT_TYPE = Column(
        String(20),
        nullable=False,
    )

    RESULT = Column(
        String(20),
        nullable=False,
    )

    REASON = Column(String(500))

    CREATED_AT = Column(
        DateTime,
        server_default=func.now(),
    )

    LABEL = relationship(
        "Label",
        back_populates="AUDITS",
    )
