from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKeyConstraint,
    Identity,
    Integer,
    PrimaryKeyConstraint,
    String,
    Unicode,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import RealEstateBase as Base

if TYPE_CHECKING:
    from .lead_models import LeadsInfo


class ClientCalls(Base):
    __tablename__ = "mini_client_calls"
    __table_args__ = (
        ForeignKeyConstraint(
            ["lead_id"],
            ["mini_leads_info.lead_id"],
            name="FK__client_ca__lead___5772F790",
        ),
        PrimaryKeyConstraint("call_id", name="PK__client_c__427DCE68CC7A9CF3"),
    )

    call_id = mapped_column(Integer, Identity(start=1, increment=1))
    date_added = mapped_column(DateTime, server_default=text("(getdate())"))
    lead_id = mapped_column(BigInteger)
    call_date = mapped_column(DateTime)
    call_status = mapped_column(String(50, "SQL_Latin1_General_CP1_CI_AS"))
    lead: Mapped[Optional["LeadsInfo"]] = relationship("LeadsInfo")


class ClientMeetings(Base):
    __tablename__ = "mini_client_meetings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["lead_id"],
            ["mini_leads_info.lead_id"],
            name="FK__client_me__lead___50C5FA01",
        ),
        PrimaryKeyConstraint("meeting_id", name="PK__client_m__C7B91CABC15584CE"),
    )

    meeting_id = mapped_column(Integer, Identity(start=1, increment=1))
    date_added = mapped_column(DateTime, server_default=text("(getdate())"))
    lead_id = mapped_column(BigInteger)
    meeting_date = mapped_column(DateTime)
    meeting_status = mapped_column(String(50, "SQL_Latin1_General_CP1_CI_AS"))
    lead: Mapped[Optional["LeadsInfo"]] = relationship("LeadsInfo")
