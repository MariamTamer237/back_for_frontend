from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    Identity,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Unicode,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import RealEstateBase as Base


class LeadsInfo(Base):
    __tablename__ = "mini_leads_info"
    __table_args__ = (
        PrimaryKeyConstraint("lead_id"),
        Index("UQ__leads_in__69D6850C784835C3", "lead_phone", unique=True),
    )

    lead_id = mapped_column(BigInteger, Identity(start=1, increment=1))
    lead_phone = mapped_column(
        String(50, "SQL_Latin1_General_CP1_CI_AS"), nullable=False
    )
    date_added = mapped_column(DateTime, server_default=text("(getdate())"))
    name = mapped_column(Unicode(50, "SQL_Latin1_General_CP1_CI_AS"))
    assigned_to = mapped_column(String(50, "SQL_Latin1_General_CP1_CI_AS"))
    email = mapped_column(String(50, "SQL_Latin1_General_CP1_CI_AS"))
    gender = mapped_column(String(10, "SQL_Latin1_General_CP1_CI_AS"))
    job_title = mapped_column(String(100, "SQL_Latin1_General_CP1_CI_AS"))
    lead_status = mapped_column(String(50, "SQL_Latin1_General_CP1_CI_AS"))
    lead_type = mapped_column(String(50, "SQL_Latin1_General_CP1_CI_AS"))
    lead_stage = mapped_column(String(50, "SQL_Latin1_General_CP1_CI_AS"))
