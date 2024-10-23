from operator import or_
from typing import List, Optional

from sqlalchemy import extract
from sqlalchemy.orm import Session

from ..exceptions.crud_exceptions import EntityNotFoundError
from ..models import actions_models, lead_models
from ..schemas import actions_schemas
from . import lead_crud


def get_sales_calls(
    db: Session,
    search: Optional[actions_schemas.SalesActionSearch] = None,
) -> List[actions_models.ClientCalls]:
    query = db.query(actions_models.ClientCalls)
    if search:
        if search.search:
            query = query.filter(
                or_(
                    lead_models.LeadsInfo.name.ilike(f"%{search.search}%"),
                    lead_models.LeadsInfo.lead_phone.ilike(f"%{search.search}%"),
                )
            )
        if search.dates:
            query = query.filter(
                extract("Year", actions_models.ClientCalls.call_date)
                == search.dates.year,
                extract("Month", actions_models.ClientCalls.call_date)
                == search.dates.month,
                extract("Day", actions_models.ClientCalls.call_date)
                == search.dates.day,
            )

    return query.all()


def get_sales_meetings(
    db: Session,
    search: Optional[actions_schemas.SalesActionSearch] = None,
) -> List[actions_models.ClientMeetings]:
    query = db.query(actions_models.ClientMeetings)

    if search:
        if search.search:
            query = query.filter(
                or_(
                    lead_models.LeadsInfo.name.ilike(f"%{search.search}%"),
                    lead_models.LeadsInfo.lead_phone.ilike(f"%{search.search}%"),
                )
            )
        if search.dates:
            query = query.filter(
                extract("Year", actions_models.ClientMeetings.meeting_date)
                == search.dates.year,
                extract("Month", actions_models.ClientMeetings.meeting_date)
                == search.dates.month,
                extract("Day", actions_models.ClientMeetings.meeting_date)
                == search.dates.day,
            )

    return query.all()


def get_sales_call(db: Session, call_id: int) -> actions_models.ClientCalls | None:
    return (
        db.query(actions_models.ClientCalls)
        .filter(
            actions_models.ClientCalls.call_id == call_id,
        )
        .first()
    )


def get_sales_meeting(
    db: Session, meeting_id: int
) -> actions_models.ClientMeetings | None:
    return (
        db.query(actions_models.ClientMeetings)
        .filter(
            actions_models.ClientMeetings.meeting_id == meeting_id,
        )
        .first()
    )


def get_sales_call_by_lead_id(
    db: Session, lead_id: int
) -> actions_models.ClientCalls | None:
    return (
        db.query(actions_models.ClientCalls)
        .filter(
            actions_models.ClientCalls.lead_id == lead_id,
        )
        .first()
    )


def get_sales_meeting_by_lead_id(
    db: Session, lead_id: int
) -> actions_models.ClientMeetings | None:
    return (
        db.query(actions_models.ClientMeetings)
        .filter(
            actions_models.ClientMeetings.lead_id == lead_id,
        )
        .first()
    )


def create_sales_call(
    db: Session,
    call: actions_schemas.SalesCallCreate,
) -> actions_models.ClientCalls:
    db_lead = lead_crud.get_lead(db, call.lead_id)
    if not db_lead:
        raise EntityNotFoundError("Lead", call.lead_id)
    db_call = actions_models.ClientCalls(
        lead_id=db_lead.lead_id,
        call_status=call.call_status,
        call_date=call.call_date,
    )
    db.add(db_call)
    db.flush()
    return db_call


def create_sales_meeting(
    db: Session,
    meeting: actions_schemas.SalesMeetingCreate,
) -> actions_models.ClientMeetings:
    db_lead = lead_crud.get_lead(db, meeting.lead_id)
    if not db_lead:
        raise EntityNotFoundError("Lead", meeting.lead_id)
    db_meeting = actions_models.ClientMeetings(
        lead_id=db_lead.lead_id,
        meeting_status=meeting.meeting_status,
        meeting_date=meeting.meeting_date,
    )
    db.add(db_meeting)
    db.flush()
    return db_meeting


def update_sales_call(
    db: Session,
    action: actions_schemas.SalesCallUpdate,
    call_id: int,
) -> actions_models.ClientCalls:
    call = get_sales_call(db, call_id)
    if call is None:
        raise EntityNotFoundError("Call", call_id)
    for field, value in action.model_dump(exclude_unset=True).items():
        setattr(call, field, value)

    db.add(call)
    db.flush()
    return call


def update_sales_meeting(
    db: Session,
    action: actions_schemas.SalesMeetingUpdate,
    meeting_id: int,
) -> actions_models.ClientMeetings:
    meeting = get_sales_meeting(db, meeting_id)
    if meeting is None:
        raise EntityNotFoundError("Meeting", meeting_id)
    for field, value in action.model_dump(exclude_unset=True).items():
        setattr(meeting, field, value)

    db.add(meeting)
    db.flush()
    return meeting


def delete_sales_call(
    db: Session,
    call_id: int,
) -> bool:
    db_call = get_sales_call(db, call_id)
    db.delete(db_call)
    db.flush()
    return True


def delete_sales_meeting(
    db: Session,
    meeting_id: int,
) -> bool:
    db_meetings = get_sales_meeting(db, meeting_id)
    db.delete(db_meetings)
    db.flush()
    return True
