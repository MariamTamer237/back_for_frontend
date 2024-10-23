from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from .. import constants
from ..schemas.phone_number import PhoneNumber


class LeadSearch(BaseModel):
    search: Optional[str] = None


class LeadsInfo(BaseModel):
    lead_id: int
    lead_phone: PhoneNumber
    date_added: datetime
    name: str
    gender: Optional[constants.Gender] = None
    assigned_to: str
    email: Optional[EmailStr] = None
    job_title: str
    lead_status: str
    lead_type: str
    lead_stage: str


class LeadUpdate(BaseModel):
    lead_phone: Optional[PhoneNumber] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    assigned_to: str
    job_title: str
    lead_status: str
    lead_type: str
    lead_stage: str


class CreateLeadsInfo(BaseModel):
    lead_phone: PhoneNumber
    name: str
    assigned_to: str
    email: Optional[EmailStr] = None
    gender: str
    job_title: str
    lead_status: str
    lead_type: str
    lead_stage: str
