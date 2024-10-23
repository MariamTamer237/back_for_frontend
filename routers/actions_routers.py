from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..constants import Module, Persmission
from ..crud import actions_crud as call_crud
from ..dependencies import get_db
from ..exceptions.api_exceptions import NotEnoughModuleFeaturePermissionsError
from ..exceptions.crud_exceptions import EntityNotFoundError
from ..schemas import actions_schemas as call_schemas

router = APIRouter(prefix="/actions", tags=["Actions"])


@router.get("/calls", response_model=List[call_schemas.ClientCalls])
def get_calls(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    date: Optional[date] = None,
):
    the_search: Optional[call_schemas.SalesActionSearch] = None
    if search is not None or date is not None:
        the_search = call_schemas.SalesActionSearch(
            search=search,
            dates=date,
        )
    calls = call_crud.get_sales_calls(db, the_search)
    return calls


@router.get("/meetings", response_model=List[call_schemas.ClientMeetings])
def get_meetings(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    date: Optional[date] = None,
):
    the_search: Optional[call_schemas.SalesActionSearch] = None
    if search is not None or date is not None:
        the_search = call_schemas.SalesActionSearch(
            search=search,
            dates=date,
        )
    meetings = call_crud.get_sales_meetings(
        db,
        the_search,
    )
    return meetings


@router.get("/calls/{call_id:int}", response_model=call_schemas.ClientCalls)
def get_call(
    call_id: int,
    db: Session = Depends(get_db),
):
    call = call_crud.get_sales_call(db, call_id)
    if not call:
        raise EntityNotFoundError("Call", call_id)
    return call


@router.get("/meetings/{meeting_id:int}", response_model=call_schemas.ClientMeetings)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
):
    meeting = call_crud.get_sales_meeting(db, meeting_id)
    if not meeting:
        raise EntityNotFoundError("Meeting", meeting_id)
    return meeting


@router.post("/create_call", response_model=call_schemas.ClientCalls)
def create_call(
    call: call_schemas.SalesCallCreate,
    db: Session = Depends(get_db),
):
    created_call = call_crud.create_sales_call(db, call)
    db.commit()
    return created_call


@router.post("/create_meeting", response_model=call_schemas.ClientMeetings)
def create_meeting(
    meeting: call_schemas.SalesMeetingCreate,
    db: Session = Depends(get_db),
):
    created_meeting = call_crud.create_sales_meeting(db, meeting)
    db.commit()
    return created_meeting


@router.put("/calls/update/{call_id:int}", response_model=call_schemas.ClientCalls)
def update_call(
    call_id: int,
    action: call_schemas.SalesCallUpdate,
    db: Session = Depends(get_db),
):
    updated_call = call_crud.update_sales_call(db, action, call_id)
    if not updated_call:
        raise EntityNotFoundError("call", call_id)
    db.commit()
    return updated_call


@router.put(
    "/meetings/update/{meeting_id:int}", response_model=call_schemas.ClientMeetings
)
def update_meeting(
    meeting_id: int,
    action: call_schemas.SalesMeetingUpdate,
    db: Session = Depends(get_db),
):
    updated_meeting = call_crud.update_sales_meeting(db, action, meeting_id)
    if not updated_meeting:
        raise EntityNotFoundError("meeting", meeting_id)

    db.commit()
    return updated_meeting


@router.delete("/calls/delete/{call_id:int}")
def delete_call(
    call_id: int,
    db: Session = Depends(get_db),
):
    try:
        call_crud.delete_sales_call(db, call_id)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Cannot delete that call. It is being referenced elsewhere.",
        )
    return {"detail": "call deleted"}


@router.delete("/meetings/delete/{meeting_id:int}", status_code=204)
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
):
    try:
        call_crud.delete_sales_meeting(db, meeting_id)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Cannot delete that meeting. It is being referenced elsewhere.",
        )
    return {"detail": "meeting deleted"}
