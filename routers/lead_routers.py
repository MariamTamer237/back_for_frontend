from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..constants import Module, Persmission
from ..crud import lead_crud
from ..dependencies import get_db
from ..exceptions.api_exceptions import NotEnoughModuleFeaturePermissionsError
from ..exceptions.crud_exceptions import EntityNotFoundError
from ..schemas import actions_schemas, lead_schemas

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/", response_model=lead_schemas.LeadsInfo)
def create_lead(
    lead: lead_schemas.CreateLeadsInfo,
    db: Session = Depends(get_db),
):

    lead_info = lead_crud.create_lead(db, lead)
    db.commit()
    return lead_info


@router.get("/", response_model=List[lead_schemas.LeadsInfo])
def read_leads(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    the_search: Optional[lead_schemas.LeadSearch] = None
    if search is not None:
        the_search = lead_schemas.LeadSearch(
            search=search,
        )
    leads = lead_crud.get_leads(
        db,
        the_search,
    )
    return leads


@router.get("/{lead_id:int}", response_model=lead_schemas.LeadsInfo)
def read_lead(
    lead_id: int,
    db: Session = Depends(get_db),
):
    lead = lead_crud.get_lead(db, lead_id)
    if lead is None:
        raise EntityNotFoundError("lead", lead_id)
    return lead


class LeadAction(BaseModel):
    calls: Optional[List[actions_schemas.ClientCalls]] = None
    meetings: Optional[List[actions_schemas.ClientMeetings]] = None


@router.get(
    "/lead_actions/{lead_id:int}",
    response_model=LeadAction,
)
def read_lead_actions(  # type: ignore
    lead_id: int,
    db: Session = Depends(get_db),
):

    actions = lead_crud.get_lead_actions(db, lead_id)  # type: ignore
    return actions  # type: ignore


@router.put("/{lead_id:int}", response_model=lead_schemas.LeadsInfo)
def update_lead(
    lead_id: int,
    lead: lead_schemas.LeadUpdate,
    db: Session = Depends(get_db),
):
    update_lead = lead_crud.update_lead(db, lead_id, lead)
    db.commit()
    return update_lead


@router.delete("/{lead_id:int}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
):
    lead_crud.delete_lead(db, lead_id)
    db.commit()

    return {"detail": {"msg": "Lead deleted"}, "lead_id": lead_id}


@router.put(
    "/rotate/{lead_id}/{to_id}",
    response_model=lead_schemas.LeadsInfo,
)
def rotate_lead(
    lead_id: int,
    to_id: str,
    db: Session = Depends(get_db),
):
    updated_lead = lead_crud.rotate_lead(db, lead_id, to_id)
    db.commit()
    return updated_lead
