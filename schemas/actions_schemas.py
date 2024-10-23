from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from ..schemas.lead_schemas import LeadsInfo


class SalesActionSearch(BaseModel):
    search: Optional[str] = None
    dates: Optional[date] = None


class ClientCalls(BaseModel):
    call_id: int
    date_added: datetime
    lead_id: int
    call_date: datetime
    call_status: str
    lead: Optional[LeadsInfo] = None


class ClientMeetings(BaseModel):
    meeting_id: int
    date_added: datetime
    lead_id: int
    meeting_date: datetime
    meeting_status: str
    lead: Optional[LeadsInfo] = None


class SalesCallCreate(BaseModel):
    lead_id: int
    call_status: str
    call_date: Optional[datetime] = datetime.now()


class SalesMeetingCreate(BaseModel):
    lead_id: int
    meeting_status: str
    meeting_date: Optional[datetime] = datetime.now()


class SalesActionUpdate(BaseModel):
    call_id: Optional[int] = None
    meeting_id: Optional[int] = None
    call_status_id: Optional[str] = None
    meeting_status_id: Optional[str] = None
    call_date: Optional[datetime] = None
    meeting_date: Optional[datetime] = None


class SalesCallUpdate(BaseModel):
    call_status: Optional[str] = None
    call_date: Optional[datetime] = None


class SalesMeetingUpdate(BaseModel):
    meeting_status: Optional[str] = None
    meeting_date: Optional[datetime] = None
