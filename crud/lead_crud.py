from operator import or_
from tokenize import String
from typing import List, Optional

from pydantic import EmailStr
from sqlalchemy import null, true
from sqlalchemy.orm import Query, Session

from ..exceptions.crud_exceptions import EntityAlreadyExistsError, EntityNotFoundError
from ..models import actions_models, lead_models
from ..schemas import lead_schemas
from ..schemas.phone_number import PhoneNumber


def search_leads(
    query: Query[lead_models.LeadsInfo],
    search: Optional[lead_schemas.LeadSearch],
):
    if search:
        if search.search:
            query = query.filter(
                or_(
                    lead_models.LeadsInfo.name.ilike(f"%{search.search}%"),
                    lead_models.LeadsInfo.lead_phone.ilike(f"%{search.search}%"),
                )
            )
    return query


def get_leads(
    db: Session,
    search: Optional[lead_schemas.LeadSearch] = None,
) -> List[lead_models.LeadsInfo]:
    query = db.query(lead_models.LeadsInfo)
    if search:
        query = search_leads(query, search)

    leads = query.all()
    return leads


def create_lead(
    db: Session,
    lead: lead_schemas.CreateLeadsInfo,
) -> lead_models.LeadsInfo:
    db_lead = lead_models.LeadsInfo(
        lead_phone=lead.lead_phone,
        name=lead.name,
        email=lead.email,
        gender=lead.gender,
        assigned_to=lead.assigned_to,
        job_title=lead.job_title,
        lead_status=lead.lead_status,
        lead_type=lead.lead_type,
        lead_stage=lead.lead_stage,
    )
    phone = (
        db.query(lead_models.LeadsInfo)
        .filter(lead_models.LeadsInfo.lead_phone == db_lead.lead_phone)
        .first()
    )
    if phone:
        EntityAlreadyExistsError("Lead", db_lead.lead_phone, "Phone number")
    db.add(db_lead)
    db.flush()
    return db_lead


def get_lead(db: Session, lead_id: int) -> Optional[lead_models.LeadsInfo]:
    return (
        db.query(lead_models.LeadsInfo)
        .filter(lead_models.LeadsInfo.lead_id == lead_id)
        .first()
    )


def update_lead(
    db: Session,
    lead_id: int,
    lead: lead_schemas.LeadUpdate,
) -> lead_models.LeadsInfo:
    db_lead = get_lead(
        db,
        lead_id,
    )
    if db_lead is None:
        raise EntityNotFoundError("Lead", lead_id)
    for field, value in lead.model_dump(exclude_unset=True).items():
        setattr(db_lead, field, value)

    db.flush()
    return db_lead


def delete_lead(
    db: Session,
    lead_id: int,
) -> Optional[lead_schemas.LeadsInfo]:
    db_lead = get_lead(db, lead_id)
    if not db_lead:
        raise EntityNotFoundError("Lead", lead_id)
    db.delete(db_lead)
    db.flush()
    return db_lead


def assign_lead(
    db: Session,
    lead_id: int,
    employee_name: str,
) -> Optional[lead_schemas.LeadsInfo]:
    db_lead = get_lead(db, lead_id)
    if db_lead:
        db_lead.assigned_to = employee_name
        db.flush()
    return db_lead


def unassign_lead(db: Session, lead_id: int) -> Optional[lead_schemas.LeadsInfo]:
    db_lead = get_lead(db, lead_id)
    if db_lead:
        db_lead.assigned_to = None
        db.flush()
    return db_lead


def rotate_lead(
    db: Session, lead_id: int, to_id: Optional[str]
) -> lead_models.LeadsInfo | None:

    db_lead = get_lead(db, lead_id)
    if not db_lead:
        raise EntityNotFoundError("Lead", lead_id)

    db_lead.assigned_to = to_id
    db.flush()
    return db_lead


def get_lead_actions(db: Session, lead_id: int):  # type: ignore
    call_query = (
        db.query(actions_models.ClientCalls)
        .filter(
            actions_models.ClientCalls.lead_id == lead_id,
        )
        .all()
    )
    meeting_query = (
        db.query(actions_models.ClientMeetings)
        .filter(
            actions_models.ClientMeetings.lead_id == lead_id,
        )
        .all()
    )

    if call_query and meeting_query:
        return {"calls": call_query, "meetings": meeting_query}
    elif call_query:
        return {"calls": call_query}
    elif meeting_query:
        return {"meetings": meeting_query}
    else:
        return {"calls": [], "meetings": []}  # type: ignore
